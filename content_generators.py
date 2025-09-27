"""
Content generators module for Deriv Clone application
"""
from config import DERIV_URLS, DERIV_THEME

def get_homepage_content():
    """Generate homepage content"""
    return f"""
    <div class="hero">
        <h1>Trade with Confidence</h1>
        <p>Experience the world's most advanced trading platforms with 200+ instruments</p>
        <a href="/trade/cfds" class="cta-button">Start Trading Now</a>
    </div>
    
    <div class="container">
        <div class="content-section">
            <h2 class="section-title">Welcome to Deriv Clone</h2>
            <p style="font-size: 1.2em; color: #666; margin-bottom: 30px;">
                This is a fully functional demo of the Deriv trading platform with <strong>{len(DERIV_URLS)} dynamic routes</strong> 
                generated from the real Deriv website structure.
            </p>
            
            <div class="grid">
                <div class="card">
                    <i class="fas fa-chart-line"></i>
                    <h3>Live Trading</h3>
                    <p>Access CFDs and Options with real-time market data</p>
                    <a href="/trade/cfds">Explore Trading</a>
                </div>
                <div class="card">
                    <i class="fas fa-globe"></i>
                    <h3>Global Markets</h3>
                    <p>Trade Forex, Stocks, Commodities, and Cryptocurrencies</p>
                    <a href="/markets/forex">View Markets</a>
                </div>
                <div class="card">
                    <i class="fas fa-mobile-alt"></i>
                    <h3>Trading Platforms</h3>
                    <p>MT5, Deriv X, Deriv Trader, and more</p>
                    <a href="/trading-platforms/deriv-mt5">See Platforms</a>
                </div>
                <div class="card">
                    <i class="fas fa-graduation-cap"></i>
                    <h3>Learning Center</h3>
                    <p>Academy, Blog, and Trading Resources</p>
                    <a href="/academy">Start Learning</a>
                </div>
            </div>
        </div>
    </div>
    """

def get_site_map_content():
    """Generate site map content"""
    url_sections = {}
    
    # Group URLs by category
    for url_data in DERIV_URLS[:50]:  # Show first 50 for performance
        path = url_data.get('path', '/')
        text = url_data.get('text', 'No title')
        
        if path.startswith('/markets/'):
            category = 'Markets'
        elif path.startswith('/trade/'):
            category = 'Trading'
        elif path.startswith('/trading-platforms/'):
            category = 'Platforms'
        elif path in ['/academy', '/blog', '/trading-terms-glossary']:
            category = 'Education'
        elif path in ['/help-centre', '/payment-methods']:
            category = 'Support'
        else:
            category = 'General'
        
        if category not in url_sections:
            url_sections[category] = []
        url_sections[category].append((path, text))
    
    sections_html = ""
    for category, urls in url_sections.items():
        urls_html = ""
        for path, text in urls:
            display_text = text if text and text != 'No text found' else path.split('/')[-1].title().replace('-', ' ')
            urls_html += f"""
            <div class="url-item">
                <a href="{path}">{path}</a>
                <span class="url-text">{display_text}</span>
            </div>
            """
        
        sections_html += f"""
        <div class="content-section">
            <h3 style="color: {DERIV_THEME['primary']}; margin-bottom: 20px;">{category}</h3>
            <div class="url-list">
                {urls_html}
            </div>
        </div>
        """
    
    return f"""
    <div class="container">
        <div class="content-section">
            <h1 class="section-title">Site Map</h1>
            <p style="font-size: 1.2em; color: #666; margin-bottom: 30px;">
                Explore all <strong>{len(DERIV_URLS)} available pages</strong> in this Deriv clone. 
                Each route is dynamically generated from the original Deriv website structure.
            </p>
            <div style="background: #e8f5e8; padding: 20px; border-radius: 10px; margin-bottom: 30px;">
                <p><i class="fas fa-info-circle" style="color: {DERIV_THEME['primary']};"></i> 
                <strong>Demo Features:</strong> All pages are functional with realistic content, navigation, and responsive design.</p>
            </div>
        </div>
        
        {sections_html}
        
        <div class="content-section">
            <h3 style="color: {DERIV_THEME['primary']};">API Endpoints</h3>
            <div class="url-list">
                <div class="url-item">
                    <a href="/api/urls">GET /api/urls</a>
                    <span class="url-text">Get all available URLs as JSON</span>
                </div>
            </div>
        </div>
    </div>
    """

def get_market_content(market_type):
    """Generate market-specific content"""
    market_data = {
        'forex': {
            'title': 'Forex Trading',
            'description': 'Trade major, minor, and exotic currency pairs with tight spreads',
            'instruments': [
                ('EUR/USD', '1.0825', '+0.0012', 'up'),
                ('GBP/USD', '1.2654', '-0.0023', 'down'),
                ('USD/JPY', '149.25', '+0.45', 'up'),
                ('AUD/USD', '0.6543', '+0.0008', 'up')
            ]
        },
        'stocks': {
            'title': 'Stock Trading',
            'description': 'Access global stock markets with fractional shares',
            'instruments': [
                ('AAPL', '$175.43', '+2.15', 'up'),
                ('GOOGL', '$127.85', '-1.23', 'down'),
                ('TSLA', '$242.65', '+5.43', 'up'),
                ('MSFT', '$378.91', '+1.87', 'up')
            ]
        },
        'commodities': {
            'title': 'Commodities Trading',
            'description': 'Trade precious metals, energy, and agricultural commodities',
            'instruments': [
                ('Gold', '$1,975.45', '+12.35', 'up'),
                ('Silver', '$23.87', '-0.45', 'down'),
                ('Oil (WTI)', '$78.92', '+1.23', 'up'),
                ('Copper', '$3.87', '+0.05', 'up')
            ]
        },
        'cryptocurrencies': {
            'title': 'Cryptocurrency Trading',
            'description': 'Trade popular cryptocurrencies 24/7',
            'instruments': [
                ('BTC/USD', '$43,250.00', '+1,250.00', 'up'),
                ('ETH/USD', '$2,345.67', '+87.23', 'up'),
                ('ADA/USD', '$0.4523', '-0.0123', 'down'),
                ('DOT/USD', '$6.789', '+0.234', 'up')
            ]
        }
    }
    
    data = market_data.get(market_type, {
        'title': f'{market_type.title()} Trading',
        'description': f'Trade {market_type} with competitive spreads and advanced tools.',
        'instruments': [('Sample', '100.00', '+1.00', 'up')]
    })
    
    table_rows = ""
    for instrument, price, change, direction in data['instruments']:
        price_class = 'price-up' if direction == 'up' else 'price-down'
        table_rows += f"""
        <tr>
            <td>{instrument}</td>
            <td class="{price_class}">{price}</td>
            <td class="{price_class}">{change}</td>
        </tr>
        """
    
    return f"""
    <div class="container">
        <div class="content-section">
            <h1 class="section-title">{data['title']}</h1>
            <p style="font-size: 1.2em; color: #666; margin-bottom: 30px;">{data['description']}</p>
            
            <table class="market-table">
                <thead>
                    <tr>
                        <th>Instrument</th>
                        <th>Price</th>
                        <th>Change</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
            
            <div style="margin-top: 40px; text-align: center;">
                <a href="/trade/cfds" class="cta-button">Start Trading {data['title'].split()[0]}</a>
            </div>
        </div>
    </div>
    """

def get_generic_content(path, text):
    """Generate generic content for any page"""
    clean_title = text if text and text != 'No text found' else path.split('/')[-1].replace('-', ' ').title()
    
    return f"""
    <div class="container">
        <div class="content-section">
            <h1 class="section-title">{clean_title}</h1>
            <p style="font-size: 1.2em; color: #666; margin-bottom: 30px;">
                Welcome to <strong>{clean_title}</strong>. This is a demo page generated from the Deriv URL structure.
            </p>
            
            <div class="grid">
                <div class="card">
                    <i class="fas fa-info-circle"></i>
                    <h3>Page Information</h3>
                    <p><strong>Path:</strong> {path}<br>
                       <strong>Original Text:</strong> {text}<br>
                       <strong>Demo Version:</strong> Fully functional</p>
                </div>
                <div class="card">
                    <i class="fas fa-sitemap"></i>
                    <h3>Site Navigation</h3>
                    <p>Explore other sections of the site using the navigation menu above.</p>
                    <a href="/site-map">View Site Map</a>
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 40px;">
                <a href="/" class="cta-button">← Back to Home</a>
            </div>
        </div>
    </div>
    """

