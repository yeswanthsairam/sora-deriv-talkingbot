#!/usr/bin/env python3
"""
Fixed version of Deriv URL filter to capture ALL deriv URLs
"""

def filter_all_deriv_urls(input_file, output_file):
    """
    Filter ALL URLs that contain 'deriv' in the domain from the input file
    """
    all_deriv_urls = []
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Filter URLs containing 'deriv' in domain
    for line in lines:
        line = line.strip()
        # Skip empty lines and comment lines
        if line and not line.startswith('#') and 'deriv' in line and line.startswith('https://'):
            all_deriv_urls.append(line)
    
    # Save to output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("# ALL URLs containing 'deriv' domain\n")
        file.write("# " + "="*50 + "\n")
        file.write(f"# Total URLs found: {len(all_deriv_urls)}\n")
        file.write("# Generated from: all_internal_urls_simple.txt\n\n")
        
        # Write as a Python list format
        file.write("all_deriv_urls = [\n")
        for i, url in enumerate(all_deriv_urls):
            if i == len(all_deriv_urls) - 1:  # Last item
                file.write(f'    "{url}"\n')
            else:
                file.write(f'    "{url}",\n')
        file.write("]\n\n")
        
        # Also write as simple numbered list
        file.write("# Simple numbered list:\n")
        file.write("# " + "-"*30 + "\n")
        for i, url in enumerate(all_deriv_urls, 1):
            file.write(f"{i}. {url}\n")
    
    return all_deriv_urls

def categorize_all_deriv_urls(deriv_urls):
    """
    Categorize ALL the deriv URLs by subdomain
    """
    categories = {
        'main_deriv_com': [],
        'api_deriv_com': [],
        'bot_deriv_com': [],
        'community_deriv_com': [],
        'docs_deriv_com': [],
        'login_deriv_com': [],
        'region_assets_deriv_com': [],
        'smarttrader_deriv_com': [],
        'other_deriv': []
    }
    
    for url in deriv_urls:
        if 'api.deriv.com' in url:
            categories['api_deriv_com'].append(url)
        elif 'bot.deriv.com' in url:
            categories['bot_deriv_com'].append(url)
        elif 'community.deriv.com' in url:
            categories['community_deriv_com'].append(url)
        elif 'docs.deriv.com' in url:
            categories['docs_deriv_com'].append(url)
        elif 'login.deriv.com' in url:
            categories['login_deriv_com'].append(url)
        elif 'region-assets.deriv.com' in url:
            categories['region_assets_deriv_com'].append(url)
        elif 'smarttrader.deriv.com' in url:
            categories['smarttrader_deriv_com'].append(url)
        elif 'deriv.com' in url:
            categories['main_deriv_com'].append(url)
        else:
            categories['other_deriv'].append(url)
    
    return categories

def main():
    input_file = 'separated_urls/all_internal_urls_simple.txt'
    output_file = 'separated_urls/complete_deriv_urls_list.txt'
    python_file = 'separated_urls/complete_deriv_urls.py'
    
    print("🔍 Filtering ALL URLs containing 'deriv' domain...")
    
    # Filter ALL deriv URLs
    all_deriv_urls = filter_all_deriv_urls(input_file, output_file)
    
    print(f"✅ Found {len(all_deriv_urls)} total URLs containing 'deriv'")
    
    # Categorize URLs
    print("📁 Categorizing URLs by subdomain...")
    categories = categorize_all_deriv_urls(all_deriv_urls)
    
    # Print detailed summary
    print("\n📊 Detailed breakdown by subdomain:")
    total_found = 0
    for category, urls in categories.items():
        if urls:
            subdomain = category.replace('_', '.').replace('deriv.com', 'deriv.com')
            print(f"   • {subdomain}: {len(urls)} URLs")
            total_found += len(urls)
    
    print(f"\n🔢 Total: {total_found} URLs")
    
    # Create the complete Python module
    with open(python_file, 'w', encoding='utf-8') as file:
        file.write('"""\nComplete Deriv URLs List\nAll URLs containing "deriv" domain\n"""\n\n')
        
        # Write categorized lists
        for category, urls in categories.items():
            if urls:
                file.write(f"# {category.upper().replace('_', ' ')}\n")
                file.write(f"{category} = [\n")
                for i, url in enumerate(urls):
                    if i == len(urls) - 1:
                        file.write(f'    "{url}"\n')
                    else:
                        file.write(f'    "{url}",\n')
                file.write("]\n\n")
        
        # Write combined list
        file.write("# ALL DERIV URLs COMBINED\n")
        file.write("all_deriv_urls = [\n")
        for i, url in enumerate(all_deriv_urls):
            if i == len(all_deriv_urls) - 1:
                file.write(f'    "{url}"\n')
            else:
                file.write(f'    "{url}",\n')
        file.write("]\n\n")
        
        file.write(f"# Statistics\n")
        file.write(f"total_deriv_urls = {len(all_deriv_urls)}\n")
        for category, urls in categories.items():
            if urls:
                file.write(f"{category}_count = {len(urls)}\n")
        
        file.write(f'\nprint(f"Loaded {{len(all_deriv_urls)}} total Deriv URLs")\n')
    
    print(f"\n📁 Files created:")
    print(f"   • {output_file} - Complete list with details")
    print(f"   • {python_file} - Python module with categorized lists")
    
    return all_deriv_urls, categories

if __name__ == '__main__':
    all_urls, categories = main()


