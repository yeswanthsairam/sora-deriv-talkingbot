import asyncio
import numpy as np
import pickle
from typing import Literal
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.retrievers import BaseRetriever
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from sentence_transformers import CrossEncoder
from langchain_chroma import Chroma
from dotenv import load_dotenv
import os

load_dotenv()

# ------------------- Load Indexes -------------------
try:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vectorstore = Chroma(embedding_function=embeddings, persist_directory="deriv_vectorstore")
    
    if os.path.exists("deriv_bm25.pkl"):
        with open("deriv_bm25.pkl", "rb") as f:
            bm25, bm25_docs = pickle.load(f)
    else:
        print("Warning: deriv_bm25.pkl not found. Creating dummy BM25...")
        from rank_bm25 import BM25Okapi
        bm25_docs = []
        bm25 = BM25Okapi([[]])  # Dummy BM25
except Exception as e:
    print(f"Error loading indexes: {e}")
    # Create fallback components
    embeddings = None
    vectorstore = None
    bm25 = None
    bm25_docs = []

# ------------------- Hybrid Retriever -------------------
class HybridRetriever:
    def __init__(self, vectorstore, bm25, bm25_docs, k_dense=5, k_sparse=5, lambda_dense=0.6):
        self.vectorstore = vectorstore
        self.bm25 = bm25
        self.bm25_docs = bm25_docs
        self.k_dense = k_dense
        self.k_sparse = k_sparse
        self.lambda_dense = lambda_dense

    async def get_relevant_documents(self, query):
        if not self.vectorstore or not self.bm25:
            # Fallback: return empty list if components not loaded
            return []
            
        loop = asyncio.get_event_loop()
        # Run dense + sparse in parallel using loop.run_in_executor
        dense_task = loop.run_in_executor(None, self._dense_search, query)
        sparse_task = loop.run_in_executor(None, self._sparse_search, query)
        dense_docs_scores, sparse_docs_scores = await asyncio.gather(dense_task, sparse_task)
        
        # Merge scores
        merged = {}
        for d, s in dense_docs_scores:
            merged[d.page_content] = {"doc": d, "score": self.lambda_dense * s}
        for d, s in sparse_docs_scores:
            if d.page_content in merged:
                merged[d.page_content]["score"] += (1 - self.lambda_dense) * s
            else:
                merged[d.page_content] = {"doc": d, "score": (1 - self.lambda_dense) * s}
        ranked = sorted(merged.values(), key=lambda x: x["score"], reverse=True)
        return [m["doc"] for m in ranked]

    def _dense_search(self, query):
        try:
            dense_res = self.vectorstore.similarity_search_with_score(query, k=self.k_dense)
            return self._normalize([(doc, 1 / (1 + score)) for doc, score in dense_res])
        except:
            return []

    def _sparse_search(self, query):
        try:
            tokenized_query = query.split()
            scores = self.bm25.get_scores(tokenized_query)
            topk_idx = np.argsort(scores)[::-1][:self.k_sparse]
            return self._normalize([(self.bm25_docs[i], float(scores[i])) for i in topk_idx])
        except:
            return []

    def _normalize(self, docs_scores):
        if not docs_scores:
            return []
        vals = np.array([s for (_, s) in docs_scores], dtype=float)
        if np.ptp(vals) == 0:
            return [(d, 1.0) for d, _ in docs_scores]
        n = (vals - vals.min()) / np.ptp(vals)
        return [(docs_scores[i][0], float(n[i])) for i in range(len(docs_scores))]

# ------------------- Reranker -------------------
try:
    reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
except Exception as e:
    print(f"Warning: Could not load reranker: {e}")
    reranker = None

async def rerank(query, docs, top_k=5):
    if not reranker or not docs:
        return docs[:top_k]  # Return first top_k if reranker fails
    
    try:
        loop = asyncio.get_event_loop()
        pairs = [(query, d.page_content) for d in docs]
        scores = await loop.run_in_executor(None, reranker.predict, pairs)
        idx = np.argsort(scores)[::-1][:top_k]
        return [docs[i] for i in idx]
    except:
        return docs[:top_k]

# ------------------- Custom Retriever for Tool -------------------
class CustomHybridRetriever(BaseRetriever):
    """Custom hybrid retriever that combines dense and sparse search"""
    
    class Config:
        arbitrary_types_allowed = True

    def __init__(self, vectorstore, bm25, bm25_docs, k_dense=5, k_sparse=5, lambda_dense=0.6, **kwargs):
        super().__init__(**kwargs)
        # Use object.__setattr__ to bypass Pydantic validation during init
        object.__setattr__(self, 'vectorstore', vectorstore)
        object.__setattr__(self, 'bm25', bm25)
        object.__setattr__(self, 'bm25_docs', bm25_docs)
        object.__setattr__(self, 'k_dense', k_dense)
        object.__setattr__(self, 'k_sparse', k_sparse)
        object.__setattr__(self, 'lambda_dense', lambda_dense)
        object.__setattr__(self, 'hybrid_retriever', HybridRetriever(vectorstore, bm25, bm25_docs, k_dense, k_sparse, lambda_dense))

    def _get_relevant_documents(self, query: str) -> list[Document]:
        """Synchronous version - not implemented as we use async version"""
        raise NotImplementedError("Use async _aget_relevant_documents instead")

    async def _aget_relevant_documents(self, query: str) -> list[Document]:
        candidates = await self.hybrid_retriever.get_relevant_documents(query)
        top_docs = await rerank(query, candidates, top_k=5)
        return top_docs

# ------------------- Retrieval Tool -------------------
@tool
async def retrieve_context(query: str) -> str:
    """Retrieve relevant context from documents for the query."""
    try:
        retriever = CustomHybridRetriever(vectorstore, bm25, bm25_docs)
        docs = await retriever._aget_relevant_documents(query)
        if docs:
            return "\n\n".join([doc.page_content for doc in docs])
        else:
            return "No relevant context found."
    except Exception as e:
        print(f"Error in retrieve_context: {e}")
        return "Error retrieving context."

# ------------------- LLM and Prompt -------------------
try:
    # Higher temperature for more natural, conversational responses
    # Moderate token limit suitable for voice interaction
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3, max_output_tokens=300)
except Exception as e:
    print(f"Error initializing LLM: {e}")
    llm = None

system_prompt = (
    "You are DerivBot, a helpful assistant for Deriv trading platform questions.\n\n"
    
    "CRITICAL INSTRUCTION: When a user asks ANY question about Deriv (including platforms like MT5, features, services, etc.), "
    "you MUST use the retrieve_context tool first to get accurate information. Never respond to Deriv questions without using this tool.\n\n"
    
    "PROCESS:\n"
    "1. For Deriv questions: Use retrieve_context tool with the user's query\n"
    "2. Wait for the tool response\n" 
    "3. Use that context to provide a helpful, conversational answer\n\n"
    
    "RESPONSE STYLE:\n"
    "- Keep responses conversational and friendly\n"
    "- 2-3 sentences for simple questions\n"
    "- Use the retrieved context as your primary source\n"
    "- Be enthusiastic about helping with Deriv topics"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("placeholder", "{messages}"),  # Stores all previous messages for context
])

# ------------------- LangGraph Setup -------------------
if llm:
    tools = [retrieve_context]
    tool_node = ToolNode(tools)
    model = llm.bind_tools(tools)

    def call_model(state: MessagesState):
        messages = state['messages']
        # Format messages with the system prompt
        formatted_messages = prompt.invoke({"messages": messages})
        response = model.invoke(formatted_messages)
        
        # Only provide fallback if response is empty AND no tool calls (empty content with tool calls is normal)
        if (not response.content or response.content.strip() == "") and not (hasattr(response, 'tool_calls') and response.tool_calls):
            print("⚠️ Model returned empty content with no tool calls, providing fallback")
            from langchain_core.messages import AIMessage
            response = AIMessage(content="I'd be happy to help you with Deriv! Let me get some information for you. Could you please ask about a specific Deriv platform, feature, or trading topic?")
            
        return {"messages": [response]}

    async def should_continue(state: MessagesState) -> Literal["tools", END]:
        last_message = state['messages'][-1]
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        return END

    # Define Graph
    workflow = StateGraph(MessagesState)
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", tool_node)
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    workflow.add_edge("tools", "agent")

    # Memory to store conversation history
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
else:
    app = None

# ------------------- Invoke Function -------------------
async def get_response(query: str, thread_id: str = None) -> dict:
    """
    Get response from the RAG system
    """
    if not thread_id:
        thread_id = "default"
    
    print(f"🔍 Processing query: '{query}' for thread: {thread_id}")
    
    # Fallback response if app not initialized
    if not app:
        print("❌ App not initialized!")
        return {
            "response": "I'm sorry, the system is not properly initialized. Please check the configuration and try again.",
            "thread_id": thread_id
        }
    
    print("✅ App is initialized, invoking...")
    
    try:
        config = {"configurable": {"thread_id": thread_id}}
        # Append new query to state; previous messages are already stored
        final_state = await app.ainvoke(
            {"messages": [HumanMessage(content=query)]},
            config=config
        )
        
        # Get the response content and ensure it's not empty
        response_content = final_state["messages"][-1].content
        
        # Fallback for empty final responses (rare but just in case)
        if not response_content or response_content.strip() == "":
            print("⚠️ Empty final response detected, providing fallback")
            response_content = "I understand your question about Deriv! Let me make sure I give you accurate information. Could you please rephrase your question about Deriv's platforms, trading features, or services?"
        
        return {
            "response": response_content.strip(),
            "thread_id": thread_id
        }
    except Exception as e:
        print(f"❌ Error in get_response: {e}")
        import traceback
        traceback.print_exc()
        return {
            "response": f"I encountered an error: {str(e)}. Please try again.",
            "thread_id": thread_id
        }

# Test function
async def test_response():
    """Test function to verify the system works"""
    result = await get_response("What is Deriv?", "test_thread")
    print("Test response:", result)
    return result

if __name__ == "__main__":
    # Test the system
    asyncio.run(test_response())
