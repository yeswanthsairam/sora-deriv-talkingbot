"""
HTML Templates module for Deriv Clone application
"""
from flask import render_template_string
from datetime import datetime
from config import DERIV_THEME

# Base HTML template with modern Deriv design
BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page_title }} | Deriv Clone</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/styles.css">
</head>
<body>
    <!-- Demo Badge -->
    <div class="demo-badge">
        <i class="fas fa-flask"></i> DEMO MODE
    </div>
    
    <!-- Header -->
    <header class="header">
        <div class="nav-container">
            <a href="/" class="logo">
                <i class="fas fa-chart-line"></i>
                Deriv Clone
            </a>
            
            <nav>
                <ul class="main-nav">
                    <li><a href="/trade/cfds">Trade CFDs</a></li>
                    <li><a href="/trade/options">Options</a></li>
                    <li><a href="/markets/forex">Forex</a></li>
                    <li><a href="/markets/stocks">Stocks</a></li>
                    <li><a href="/trading-platforms/deriv-mt5">Platforms</a></li>
                    <li><a href="/academy">Academy</a></li>
                    <li><a href="/help-centre">Support</a></li>
                    <li><a href="/site-map">Site Map</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <!-- Main Content -->
    <main>
        {{ content | safe }}
    </main>

    <!-- Footer -->
    <footer class="footer">
        <p>&copy; {{ current_year }} Deriv Clone - Demo Version | {{ total_urls }} Pages Available</p>
    </footer>

    <!-- Floating Chat Widget -->
    <div class="chat-widget">
        <div class="chat-container" id="chatContainer">
            <div class="chat-header">
                <h3>🤖 Sora</h3>
                <p>Deriv's Voice and Text Assistant</p>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="message bot">
                    <div class="message-bubble">
                        Hi! I'm Sora, Deriv's AI assistant. You can speak to me or type your questions about Deriv trading. How can I help you today? 🎤
                    </div>
                    <div class="message-time">Just now</div>
                </div>
            </div>
            
            <div class="typing-indicator" id="typingIndicator">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
            
            <div class="chat-input-container">
                <div class="chat-input-wrapper" id="inputWrapper">
                    <button class="voice-button" id="voiceButton" title="Speak to Sora">
                        <i class="fas fa-microphone"></i>
                    </button>
                    <input type="text" class="chat-input" id="chatInput" 
                           placeholder="Ask about trading, platforms, or anything Deriv-related...">
                    <button class="send-button" id="sendButton" title="Send message">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
            </div>
            
            <div class="chat-status">
                <span class="status-online">● Online</span> - Powered by AI
            </div>
        </div>
        
        <button class="chat-button" id="chatToggle" title="Chat with Sora">
            <i class="fas fa-comments"></i>
        </button>
    </div>

    <script src="/static/js/chatbot.js"></script>
</body>
</html>
"""

def render_page(page_title, content, total_urls=0):
    """Render a page with the base template"""
    template_vars = {
        'page_title': page_title,
        'content': content,
        'theme': DERIV_THEME,
        'current_year': datetime.now().year,
        'total_urls': total_urls
    }
    
    return render_template_string(BASE_TEMPLATE, **template_vars)
