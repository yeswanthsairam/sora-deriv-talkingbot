"""
Main Flask application for Deriv Clone
"""
from flask import Flask
from config import DERIV_URLS
from routes import register_routes, create_routes

def create_app():
    """Create and configure Flask app"""
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    
    # Register static routes
    register_routes(app)
    
    # Create dynamic routes
    create_routes(app)
    
    return app

def main():
    """Main function to run the application"""
    app = create_app()
    
    print("🚀 Starting Deriv Clone - Complete Demo Platform")
    print("=" * 70)
    print("📍 URL: http://localhost:8081")
    print(f"📊 Loaded URLs: {len(DERIV_URLS)}")
    print("🎯 Features:")
    print("  ✓ Dynamic routing based on real Deriv URLs")
    print("  ✓ Responsive modern design")
    print("  ✓ Market data simulation")
    print("  ✓ Complete site navigation")
    print("  ✓ Voice-enabled AI chatbot (Sora)")
    print("  ✓ API endpoints")
    print("💡 Access /site-map to see all available pages")
    print("🎤 Click the chat button to talk to Sora!")
    print("=" * 70)
    
    app.run(
        host='0.0.0.0',
        port=8081,
        debug=True,
        threaded=True
    )

if __name__ == '__main__':
    main()