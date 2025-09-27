# Deriv RAG Voice Bot Setup Guide

## ✅ Status: WORKING!

Your Flask app is now ready to run! All dependencies are installed and the RAG system is functioning properly.

## 🚀 How to Run

### Option 1: Direct Run
```bash
cd /Users/ychinnapurapu/Deriv
python3 flaskapp.py
```

### Option 2: With Environment Variables (Recommended)
```bash
cd /Users/ychinnapurapu/Deriv
export GOOGLE_API_KEY=your_api_key_here
python3 flaskapp.py
```

## 🌐 Access the App

Once running, open your browser and navigate to:
```
http://localhost:5000
```

## 🎯 Features Available

### 🎙️ Voice Interface
- **Speech-to-Text**: Click the microphone button to speak your queries
- **Text-to-Speech**: The bot will speak responses back to you
- **Web Speech API**: Uses browser's built-in speech capabilities

### 💬 Chat Interface  
- **Real-time Chat**: Type or speak your questions
- **Context Awareness**: Maintains conversation history
- **RAG-Powered**: Retrieves information from Deriv knowledge base

### 📚 Knowledge Base
- **200+ Deriv Assets**: Information about trading options
- **Trading Platforms**: Details about MT5, cTrader, Deriv X, etc.
- **Trading Strategies**: Guidance on various trading approaches
- **Account Management**: Help with deposits, withdrawals, etc.

## 🔧 Technical Stack

- **Backend**: Quart (Async Flask)
- **RAG System**: LangGraph + Google Gemini
- **Vector Store**: ChromaDB
- **Search**: Hybrid (Dense + Sparse) retrieval with reranking
- **Voice**: Web Speech API (browser-based)

## ⚠️ Requirements

### API Keys Needed:
1. **Google API Key**: Required for Gemini AI
   - Get from: https://makersuite.google.com/app/apikey
   - Set as: `GOOGLE_API_KEY` environment variable

### Optional Files:
- `deriv_vectorstore/`: ChromaDB vector database (auto-created if missing)
- `deriv_bm25.pkl`: BM25 sparse retriever (system works without it)

## 🎨 Usage Examples

### Voice Commands:
- "What is Deriv?"
- "How do I trade cryptocurrency?"
- "Tell me about Deriv MT5"
- "What are the trading fees?"

### Chat Examples:
- "Explain the different trading platforms"
- "How do I make a deposit?"
- "What is copy trading?"

## 🛠️ Troubleshooting

### Port Already in Use:
```bash
# Kill process using port 5000
lsof -ti:5000 | xargs kill -9
```

### Missing Dependencies:
```bash
pip3 install -r requirements.txt
```

### API Key Issues:
- Make sure `GOOGLE_API_KEY` is set
- Check API key permissions and quotas

## 📊 Testing

Run the test suite to verify everything works:
```bash
python3 test_rag_agent.py
```

## 🎉 Success Indicators

✅ RAG Agent: PASS
✅ Flask App: PASS  
✅ Voice Interface: Ready
✅ Knowledge Base: Loaded
✅ All Dependencies: Installed

**Your Deriv RAG Voice Bot is ready to use!**

---

*Last updated: $(date)*

