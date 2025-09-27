#!/usr/bin/env python3
"""
Filter URLs starting with 'https://deriv' from internal URLs file
"""

def filter_deriv_urls(input_file, output_file):
    """
    Filter URLs that start with 'https://deriv' from the input file
    and save them to a list in the output file
    """
    deriv_urls = []
    
    # Read the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    # Filter URLs starting with 'https://deriv'
    for line in lines:
        line = line.strip()
        # Skip empty lines and comment lines
        if line and not line.startswith('#') and line.startswith('https://deriv'):
            deriv_urls.append(line)
    
    # Save to output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("# URLs starting with 'https://deriv'\n")
        file.write("# " + "="*50 + "\n")
        file.write(f"# Total URLs found: {len(deriv_urls)}\n")
        file.write("# Generated from: all_internal_urls_simple.txt\n\n")
        
        # Write as a Python list format
        file.write("deriv_urls = [\n")
        for i, url in enumerate(deriv_urls):
            if i == len(deriv_urls) - 1:  # Last item
                file.write(f'    "{url}"\n')
            else:
                file.write(f'    "{url}",\n')
        file.write("]\n\n")
        
        # Also write as simple list
        file.write("# Simple list format:\n")
        file.write("# " + "-"*30 + "\n")
        for i, url in enumerate(deriv_urls, 1):
            file.write(f"{i}. {url}\n")
    
    return deriv_urls

def categorize_deriv_urls(deriv_urls):
    """
    Categorize the deriv URLs by subdomain
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
        if url.startswith('https://deriv.com'):
            categories['main_deriv_com'].append(url)
        elif url.startswith('https://api.deriv.com'):
            categories['api_deriv_com'].append(url)
        elif url.startswith('https://bot.deriv.com'):
            categories['bot_deriv_com'].append(url)
        elif url.startswith('https://community.deriv.com'):
            categories['community_deriv_com'].append(url)
        elif url.startswith('https://docs.deriv.com'):
            categories['docs_deriv_com'].append(url)
        elif url.startswith('https://login.deriv.com'):
            categories['login_deriv_com'].append(url)
        elif url.startswith('https://region-assets.deriv.com'):
            categories['region_assets_deriv_com'].append(url)
        elif url.startswith('https://smarttrader.deriv.com'):
            categories['smarttrader_deriv_com'].append(url)
        else:
            categories['other_deriv'].append(url)
    
    return categories

def create_categorized_file(categories, output_file):
    """
    Create a file with categorized deriv URLs
    """
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("# Categorized Deriv URLs\n")
        file.write("# " + "="*50 + "\n\n")
        
        total_urls = sum(len(urls) for urls in categories.values())
        file.write(f"# Total URLs: {total_urls}\n\n")
        
        for category, urls in categories.items():
            if urls:  # Only write categories that have URLs
                file.write(f"# {category.upper().replace('_', ' ')}\n")
                file.write(f"# Count: {len(urls)}\n")
                file.write("# " + "-"*30 + "\n")
                
                file.write(f"{category} = [\n")
                for i, url in enumerate(urls):
                    if i == len(urls) - 1:  # Last item
                        file.write(f'    "{url}"\n')
                    else:
                        file.write(f'    "{url}",\n')
                file.write("]\n\n")

def main():
    input_file = 'separated_urls/all_internal_urls_simple.txt'
    output_file = 'separated_urls/deriv_urls_list.txt'
    categorized_file = 'separated_urls/deriv_urls_categorized.txt'
    
    print("🔍 Filtering URLs starting with 'https://deriv'...")
    
    # Filter deriv URLs
    deriv_urls = filter_deriv_urls(input_file, output_file)
    
    print(f"✅ Found {len(deriv_urls)} URLs starting with 'https://deriv'")
    
    # Categorize URLs
    print("📁 Categorizing URLs by subdomain...")
    categories = categorize_deriv_urls(deriv_urls)
    
    # Create categorized file
    create_categorized_file(categories, categorized_file)
    
    # Print summary
    print("\n📊 Summary by subdomain:")
    for category, urls in categories.items():
        if urls:
            print(f"   • {category.replace('_', '.')}: {len(urls)} URLs")
    
    print(f"\n📁 Files created:")
    print(f"   • {output_file} - Deriv URLs as Python list")
    print(f"   • {categorized_file} - URLs categorized by subdomain")
    
    # Also create a simple Python list file for easy import
    python_list_file = 'separated_urls/deriv_urls.py'
    with open(python_list_file, 'w', encoding='utf-8') as file:
        file.write('"""\nDeriv URLs List\nFiltered URLs starting with "https://deriv"\n"""\n\n')
        file.write("# All Deriv URLs\n")
        file.write("all_deriv_urls = [\n")
        for i, url in enumerate(deriv_urls):
            if i == len(deriv_urls) - 1:
                file.write(f'    "{url}"\n')
            else:
                file.write(f'    "{url}",\n')
        file.write("]\n\n")
        
        file.write(f"# Total count: {len(deriv_urls)} URLs\n")
        file.write(f"print(f'Loaded {{len(all_deriv_urls)}} Deriv URLs')\n")
    
    print(f"   • {python_list_file} - Python module for easy import")
    
    return deriv_urls

if __name__ == '__main__':
    deriv_urls = main()


