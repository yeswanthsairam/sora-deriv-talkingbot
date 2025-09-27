import scrapy
import json
from urllib.parse import urljoin, urlparse
from scrapy.crawler import CrawlerProcess
import logging

class DerivUrlSpider(scrapy.Spider):
    name = 'deriv_urls'
    start_urls = ['https://deriv.com/']
    
    # Configure custom settings
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 1,  # Be respectful
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 1,
        'FEEDS': {
            'deriv_urls.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'indent': 2,
            },
        }
    }
    
    def __init__(self):
        self.found_urls = set()
        self.internal_urls = []
        self.external_urls = []
        self.email_links = []
        self.phone_links = []
        
    def parse(self, response):
        """Parse the main page and extract all URLs"""
        
        # Extract all links from the page
        links = response.css('a::attr(href)').getall()
        
        # Also look for links in other attributes and elements
        additional_links = []
        additional_links.extend(response.css('link::attr(href)').getall())
        additional_links.extend(response.css('script::attr(src)').getall())
        additional_links.extend(response.css('img::attr(src)').getall())
        additional_links.extend(response.css('iframe::attr(src)').getall())
        
        all_links = links + additional_links
        
        for link in all_links:
            if link:
                # Clean and normalize the URL
                absolute_url = urljoin(response.url, link.strip())
                
                if absolute_url not in self.found_urls:
                    self.found_urls.add(absolute_url)
                    
                    # Categorize the URL
                    parsed_url = urlparse(absolute_url)
                    base_domain = 'deriv.com'
                    
                    # Create link info
                    link_info = {
                        'url': absolute_url,
                        'text': self.get_link_text(response, link),
                        'type': self.categorize_link(absolute_url),
                        'domain': parsed_url.netloc,
                        'path': parsed_url.path,
                        'found_on_page': response.url
                    }
                    
                    # Categorize URLs
                    if parsed_url.scheme in ['mailto']:
                        self.email_links.append(link_info)
                    elif parsed_url.scheme in ['tel']:
                        self.phone_links.append(link_info)
                    elif base_domain in parsed_url.netloc or not parsed_url.netloc:
                        self.internal_urls.append(link_info)
                    else:
                        self.external_urls.append(link_info)
        
        # Also extract any URLs from text content (like JavaScript variables)
        script_content = response.css('script::text').getall()
        for script in script_content:
            urls_in_script = self.extract_urls_from_text(script)
            for url in urls_in_script:
                if url not in self.found_urls:
                    self.found_urls.add(url)
                    parsed_url = urlparse(url)
                    link_info = {
                        'url': url,
                        'text': 'Found in script',
                        'type': 'script_url',
                        'domain': parsed_url.netloc,
                        'path': parsed_url.path,
                        'found_on_page': response.url
                    }
                    if 'deriv.com' in parsed_url.netloc or not parsed_url.netloc:
                        self.internal_urls.append(link_info)
                    else:
                        self.external_urls.append(link_info)
        
        # Yield the results
        yield {
            'page_url': response.url,
            'total_urls_found': len(self.found_urls),
            'internal_urls': self.internal_urls,
            'external_urls': self.external_urls,
            'email_links': self.email_links,
            'phone_links': self.phone_links,
            'summary': {
                'internal_count': len(self.internal_urls),
                'external_count': len(self.external_urls),
                'email_count': len(self.email_links),
                'phone_count': len(self.phone_links),
                'total_count': len(self.found_urls)
            }
        }
    
    def get_link_text(self, response, href):
        """Get the text associated with a link"""
        try:
            # Find link elements with this href and get their text
            link_elements = response.css(f'a[href="{href}"]::text').getall()
            if link_elements:
                return ' '.join(link_elements).strip()
            
            # Also check for links with relative hrefs
            if not href.startswith('http'):
                link_elements = response.css(f'a[href="{href}"]::text').getall()
                if link_elements:
                    return ' '.join(link_elements).strip()
            
            return 'No text found'
        except:
            return 'Error extracting text'
    
    def categorize_link(self, url):
        """Categorize the type of link"""
        parsed = urlparse(url)
        path = parsed.path.lower()
        
        if parsed.scheme == 'mailto':
            return 'email'
        elif parsed.scheme == 'tel':
            return 'phone'
        elif any(ext in path for ext in ['.pdf', '.doc', '.docx', '.xls', '.xlsx']):
            return 'document'
        elif any(ext in path for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp']):
            return 'image'
        elif any(ext in path for ext in ['.js', '.css']):
            return 'asset'
        elif any(keyword in path for keyword in ['/api/', '/v1/', '/v2/', '/v3/']):
            return 'api'
        elif 'social' in parsed.netloc or any(domain in parsed.netloc for domain in ['facebook.com', 'twitter.com', 'linkedin.com', 'youtube.com', 'instagram.com']):
            return 'social_media'
        else:
            return 'page'
    
    def extract_urls_from_text(self, text):
        """Extract URLs from text content"""
        import re
        url_pattern = r'https?://[^\s<>"]{2,}'
        return re.findall(url_pattern, text)

def run_spider():
    """Function to run the spider"""
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'LOG_LEVEL': 'INFO'
    })
    
    process.crawl(DerivUrlSpider)
    process.start()

if __name__ == '__main__':
    print("Starting Deriv.com URL extraction...")
    print("This will create a deriv_urls.json file with all found URLs")
    print("-" * 50)
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    
    # Run the spider
    run_spider()
    
    print("\nURL extraction completed!")
    print("Check the 'deriv_urls.json' file for results.")
