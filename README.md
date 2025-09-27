# 🤖 Sora - Deriv AI Trading Assistant

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**Sora** is an AI-powered voice trading assistant for the Deriv platform, featuring a comprehensive RAG (Retrieval-Augmented Generation) chatbot with voice capabilities, real-time market simulation, and intelligent trading assistance.

## 🌟 Features

### 🎙️ Voice Interface
- **Speech-to-Text**: Click the microphone button to speak your queries
- **Text-to-Speech**: The bot responds with voice feedback
- **Web Speech API**: Browser-based speech capabilities
- **Real-time Voice Processing**: Instant voice command recognition

### 💬 AI Chat Assistant
- **RAG-Powered**: Retrieves information from comprehensive Deriv knowledge base
- **Context Awareness**: Maintains conversation history
- **Multi-turn Conversations**: Natural dialogue flow
- **Trading Expertise**: Specialized in Deriv trading platforms and strategies

### 📊 Trading Platform Simulation
- **Dynamic Routing**: Based on real Deriv URLs structure
- **Market Data Simulation**: Real-time trading data visualization
- **Complete Site Navigation**: Full Deriv platform replica
- **Responsive Design**: Modern, mobile-friendly interface

### 📚 Knowledge Base
- **200+ Deriv Assets**: Comprehensive trading instruments
- **Platform Guides**: MT5, cTrader, Deriv X documentation
- **Trading Strategies**: Expert trading guidance
- **Account Management**: Deposits, withdrawals, verification help

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google API Key (for Gemini AI)
- Modern web browser with speech API support

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yeswanthsairam/sora-deriv-talkingbot.git
   cd sora-deriv-talkingbot
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   export GOOGLE_API_KEY=your_google_api_key_here
   ```
   Or create a `.env` file:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   Open your browser and navigate to: `http://localhost:8081`

## 🔧 Technical Architecture

### Backend Stack
- **Flask**: Web framework with async support
- **LangChain**: RAG pipeline orchestration
- **Google Gemini**: Large Language Model
- **ChromaDB**: Vector database for embeddings
- **BM25**: Sparse retrieval for hybrid search

### Frontend Stack
- **HTML5/CSS3**: Modern responsive design
- **JavaScript**: Interactive chat interface
- **Web Speech API**: Browser-based voice processing
- **Bootstrap**: UI components and styling

### AI/ML Components
- **Sentence Transformers**: Text embeddings
- **Hybrid Retrieval**: Dense + Sparse search
- **Reranking**: Improved search relevance
- **Context Management**: Conversation memory

## 📁 Project Structure

**Total Files in Repository: 20**

```
sora-deriv-talkingbot/
├── app.py                    # Main Flask application entry point
├── requirements.txt          # Python dependencies and package versions
├── .gitignore               # Git exclusions for Python projects
├── README.md                # Project documentation and setup guide
├── src/                      # Core Application Components
│   ├── config.py            #   Application configuration and theme settings
│   ├── routes.py            #   Flask route handlers and API endpoints  
│   └── templates.py         #   HTML template rendering system
├── ai/                       # Artificial Intelligence and RAG Components  
│   ├── chat_handler.py      #   Chat API endpoint and request processing
│   ├── rag_agent.py         #   RAG agent with Google Gemini integration
│   ├── rag_pipeline.py      #   RAG processing and retrieval pipeline
│   ├── voice_utils.py       #   Voice processing and speech utilities
│   └── content_generators.py #   Dynamic content generation for pages
├── data/                     # Data Files and Configuration
│   └── deriv_urls.json      #   URL configuration data for routing system
├── scrapy/                   # Web Scraping and URL Discovery Tools
│   ├── ScrapyUrls.py        #   Scrapy spider for Deriv website crawling
│   ├── scrapy.cfg           #   Scrapy project configuration file
│   └── scrapy_settings.py   #   Spider behavior and crawling settings
├── docs/                     # Project Documentation
│   ├── setup_guide.md       #   Detailed installation and setup instructions
│   └── SOLUTION_FIXED.md    #   Technical implementation documentation
└── static/                   # Frontend Static Assets
    ├── css/styles.css       #   Modern UI styling and responsive design
    └── js/chatbot.js        #   Frontend JavaScript for chat interface
```

### Folder Purposes:

- **src/** - Contains the core Flask application logic, configuration, routing, and template rendering
- **ai/** - Houses all artificial intelligence components including RAG system, chat processing, and content generation  
- **data/** - Stores configuration data files, particularly the URL routing configuration
- **scrapy/** - Contains web scraping tools used to discover and categorize Deriv website URLs
- **docs/** - Project documentation including setup guides and technical specifications
- **static/** - Frontend assets including CSS styling and JavaScript for the user interface

## 🎯 Usage Examples

### Voice Commands
- *"What is Deriv?"*
- *"How do I trade cryptocurrency?"*
- *"Tell me about Deriv MT5"*
- *"What are the trading fees?"*
- *"Explain copy trading"*

### Chat Interface
- Type questions about trading, platforms, or strategies
- Ask for account management help
- Request market analysis guidance
- Get platform navigation assistance

## 🔗 API Endpoints

- `GET /` - Main application interface
- `POST /chat` - Chat API endpoint
- `GET /site-map` - Available pages overview
- `GET /api/status` - Health check
- `POST /voice/process` - Voice processing endpoint

## 🛠️ Configuration

### Environment Variables
- `GOOGLE_API_KEY`: Required for Gemini AI integration
- `FLASK_ENV`: Set to 'development' for debug mode
- `PORT`: Custom port (default: 8081)

### Optional Configuration
- Vector database will be created automatically on first run
- BM25 index will be built from available data
- Chat history is maintained in session

## 🧪 Testing

Run the test suite to verify functionality:
```bash
python -m pytest tests/
```

For manual testing:
```bash
python test_rag_agent.py
```

## 🚨 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
lsof -ti:8081 | xargs kill -9
```

**Missing Dependencies:**
```bash
pip install -r requirements.txt --upgrade
```

**API Key Issues:**
- Verify `GOOGLE_API_KEY` is set correctly
- Check API quotas and permissions
- Ensure internet connection for API calls

**Voice Not Working:**
- Use HTTPS or localhost for speech API
- Check browser permissions for microphone
- Ensure browser supports Web Speech API

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Deriv**: For the comprehensive trading platform
- **Google Gemini**: AI model powering the assistant
- **LangChain**: RAG framework and tools
- **ChromaDB**: Vector database solution
- **Flask**: Web framework foundation

## 📞 Support

For support and questions:
- 📧 Email: [your-email@example.com]
- 💬 GitHub Issues: [Open an issue](https://github.com/yeswanthsairam/sora-deriv-talkingbot/issues)
- 📖 Documentation: Check `setup_guide.md` for detailed setup

---

**⭐ If you find this project helpful, please give it a star!**

*Built with ❤️ for the Deriv trading community*
