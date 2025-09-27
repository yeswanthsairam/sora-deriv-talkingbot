"""
Configuration module for Deriv Clone application
"""
import json

# Deriv-inspired color scheme
DERIV_THEME = {
    'primary': '#ff6544',
    'secondary': '#85acb0', 
    'dark': '#0e0e0e',
    'light': '#ffffff',
    'gray': '#999999',
    'success': '#4caf50',
    'background': '#f8f9fa'
}

def load_deriv_urls():
    """Load URLs from deriv_urls.json"""
    try:
        with open('/Users/ychinnapurapu/Deriv/deriv_urls.json', 'r') as f:
            data = json.load(f)
            if isinstance(data, list) and len(data) > 0:
                return data[0].get('internal_urls', [])
            return []
    except Exception as e:
        print(f"Error loading URLs: {e}")
        return []

# Load URLs at module import
DERIV_URLS = load_deriv_urls()
