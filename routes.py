"""
Routes module for Deriv Clone application
"""
from flask import jsonify
from config import DERIV_URLS
from templates import render_page
from content_generators import (
    get_homepage_content, 
    get_site_map_content, 
    get_market_content, 
    get_generic_content
)
from chat_handler import handle_chat

def register_routes(app):
    """Register all routes for the Flask app"""
    
    @app.route('/')
    def home():
        """Homepage route"""
        return render_page(
            "Trade with Confidence - Your Gateway to Financial Markets",
            get_homepage_content(),
            len(DERIV_URLS)
        )

    @app.route('/site-map')
    def site_map():
        """Site map route"""
        return render_page(
            "Site Map",
            get_site_map_content(),
            len(DERIV_URLS)
        )

    @app.route('/chat', methods=['POST'])
    def chat():
        """Chat endpoint for the chatbot"""
        return handle_chat()

    @app.route('/api/urls')
    def api_urls():
        """API endpoint to get all URLs as JSON"""
        return jsonify({
            'total_urls': len(DERIV_URLS),
            'urls': DERIV_URLS[:100]  # Return first 100 URLs
        })

def create_dynamic_route(path, text):
    """Create a dynamic route handler"""
    def route_handler():
        # Check if this is a market page
        if path.startswith('/markets/'):
            market_type = path.split('/')[-1]  # e.g., 'forex' from '/markets/forex'
            content = get_market_content(market_type)
        else:
            content = get_generic_content(path, text)
        
        return render_page(
            text if text and text != 'No text found' else path.replace('/', ' ').title(),
            content,
            len(DERIV_URLS)
        )
    
    return route_handler

def create_routes(app):
    """Create dynamic routes from DERIV_URLS"""
    added_routes = set()
    route_counter = 0
    
    # Add the homepage route explicitly first
    added_routes.add('/')

    for url_data in DERIV_URLS:
        path = url_data.get('path', '')  # Default to empty string for safety
        text = url_data.get('text', '')
        
        # Skip invalid paths (empty, None, or not starting with /)
        if not path or not isinstance(path, str) or len(path.strip()) == 0 or not path.strip().startswith('/'):
            print(f"Skipping invalid path: '{path}'")
            continue
            
        # Skip duplicate paths and the home route if it appears again
        if path in added_routes:
            continue
            
        added_routes.add(path)
        
        try:
            app.add_url_rule(
                path,
                endpoint=f"dynamic_route_{route_counter}",
                view_func=create_dynamic_route(path, text),
                methods=['GET']
            )
            route_counter += 1
        except Exception as e:
            print(f"Warning: Could not add route {path}: {e}")
            continue

