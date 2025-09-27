# from dotenv import load_dotenv
# load_dotenv()

# from langchain_community.document_loaders import UnstructuredURLLoader
# from separated_urls.deriv_urls import all_deriv_urls
# urls = all_deriv_urls
# loader = UnstructuredURLLoader(urls=urls)
# data = loader.load()

# from langchain.text_splitter import RecursiveCharacterTextSplitter

# # split data
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
# docs = text_splitter.split_documents(data)


# # Embedding models: https://python.langchain.com/v0.1/docs/integrations/text_embedding/
# # Let's load the Hugging Face Embedding class.  sentence_transformers


# from langchain_google_genai import GoogleGenerativeAIEmbeddings

# embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

# #vector

# from langchain_chroma import Chroma
# vectorstore = Chroma.from_documents(documents=docs, embedding=HuggingFaceEmbeddings())

# retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})


# from langchain_huggingface import HuggingFacePipeline
# from langchain.prompts import PromptTemplate
# from transformers import pipeline
# from langchain_core.output_parsers import StrOutputParser
# import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer


# #model_id = "meta-llama/Meta-Llama-3-8B"
# from langchain_google_genai import ChatGoogleGenerativeAI

# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.3, max_tokens=500)
# from langchain.chains import create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_core.prompts import ChatPromptTemplate

# system_prompt = (
#     "You are an assistant for question-answering tasks. "
#     "Use the following pieces of retrieved context to answer "
#     "the question. If you don't know the answer, say that you "
#     "don't know. Use three sentences maximum and keep the "
#     "answer concise."
#     "\n\n"
#     "{context}"
# )

# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", system_prompt),
#         ("human", "{input}"),
#     ]
# )
# question_answer_chain = create_stuff_documents_chain(llm, prompt)
# rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# import streamlit as st

# query = st.text_input("Enter your query: ")
# response = rag_chain.invoke({"input": query})

# # Making the response readable
# response = response.replace("</s>", "").strip()
# st.write("Response:", response)

# from langchain_community.document_loaders import UnstructuredURLLoader
# from separated_urls.deriv_urls import all_deriv_urls
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_google_genai import GoogleGenerativeAIEmbeddings
# from langchain_chroma import Chroma
# from dotenv import load_dotenv
# load_dotenv()

# # Step 1: Load data once
# urls = all_deriv_urls
# loader = UnstructuredURLLoader(urls=urls)
# data = loader.load()

# # Step 2: Split into chunks
# text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000)
# docs = text_splitter.split_documents(data)

# # Step 3: Create embeddings
# embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# # Step 4: Store in persistent Chroma DB
# vectorstore = Chroma.from_documents(
#     documents=docs,
#     embedding=embeddings,
#     persist_directory="deriv_vectorstore"  # <--- folder to save data
# )

# print("✅ Vectorstore built and saved to 'deriv_vectorstore'")

from langchain_community.document_loaders import UnstructuredURLLoader
from separated_urls.deriv_urls import all_deriv_urls
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from rank_bm25 import BM25Okapi
from dotenv import load_dotenv
import pickle

load_dotenv()

# Step 1: Load data once
urls = all_deriv_urls
loader = UnstructuredURLLoader(urls=urls)
data = loader.load()

# Step 2: Split into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
docs = text_splitter.split_documents(data)

# Step 3: Create embeddings (dense)
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Step 4: Store in persistent Chroma DB (dense vectorstore)
vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory="deriv_vectorstore"
)

# Step 5: Build BM25 (sparse index)
tokenized_docs = [doc.page_content.split() for doc in docs]
bm25 = BM25Okapi(tokenized_docs)

# Save BM25 + docs for later use
with open("deriv_bm25.pkl", "wb") as f:
    pickle.dump((bm25, docs), f)

print("✅ Vectorstore + BM25 index built and saved")
