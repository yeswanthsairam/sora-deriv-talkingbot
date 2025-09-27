"""
Chat handler module for Deriv Clone application
"""
from flask import jsonify, request
import uuid
import asyncio
import concurrent.futures
from ai.rag_agent import get_response

def handle_chat():
    """Handle chat endpoint for the chatbot"""
    try:
        data = request.get_json()
        query = data.get('query')
        thread_id = data.get('thread_id', str(uuid.uuid4()))
        
        print(f"📥 Chat query: '{query}' (thread: {thread_id[:8]}...)")
        
        if not query:
            return jsonify({
                "response": "Please ask me something about Deriv trading!",
                "thread_id": thread_id
            })
        
        print(f"🔍 Processing query: '{query}' for thread: {thread_id}")
        
        # Run the async get_response function synchronously
        loop = None
        try:
            # Try to get existing loop
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No running loop, create new one
            pass
        
        if loop and loop.is_running():
            # We're already in an event loop, use run_in_executor
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, get_response(query, thread_id))
                result = future.result(timeout=30)
        else:
            # No event loop running, safe to use asyncio.run
            result = asyncio.run(get_response(query, thread_id))
        
        print(f"✅ App is initialized, invoking...")
        
        if result:
            response_text = result.get('response', 'I apologize, but I could not generate a response. Please try again.')
            response_thread_id = result.get('thread_id', thread_id)
            
            print(f"📤 Bot response: '{response_text[:100]}{'...' if len(response_text) > 100 else ''}'")
            
            return jsonify({
                "response": response_text,
                "thread_id": response_thread_id
            })
        else:
            return jsonify({
                "response": "I apologize, but I'm having trouble processing your request right now. Please try again later.",
                "thread_id": thread_id
            })
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        import traceback
        traceback.print_exc()
        
        # Provide helpful error message to user
        thread_id = thread_id if 'thread_id' in locals() else str(uuid.uuid4())
        return jsonify({
            "response": "I'm sorry, I encountered an error processing your request. Please try again or ask me about Deriv trading platforms, markets, or any other trading-related questions.",
            "thread_id": thread_id
        })

