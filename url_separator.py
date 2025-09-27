#!/usr/bin/env python3
"""
URL Separator Script
Separates URLs from the scraped JSON file into different categories and files
"""

import json
import csv
from collections import defaultdict
from datetime import datetime

def load_json_data(filename):
    """Load the JSON data from the scraped file"""
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data[0]  # The data is in a list with one element

def save_urls_to_txt(urls, filename, title):
    """Save URLs to a text file"""
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"{title}\n")
        file.write("=" * len(title) + "\n")
        file.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Total URLs: {len(urls)}\n\n")
        
        for i, url_data in enumerate(urls, 1):
            if isinstance(url_data, dict):
                file.write(f"{i}. {url_data['url']}\n")
                if url_data.get('text') and url_data['text'] != 'No text found':
                    file.write(f"   Text: {url_data['text']}\n")
                if url_data.get('type'):
                    file.write(f"   Type: {url_data['type']}\n")
                file.write("\n")
            else:
                file.write(f"{i}. {url_data}\n")

def save_urls_to_csv(urls, filename):
    """Save URLs to a CSV file"""
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        if urls and isinstance(urls[0], dict):
            fieldnames = ['url', 'text', 'type', 'domain', 'path', 'found_on_page']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(urls)
        else:
            writer = csv.writer(file)
            writer.writerow(['URL'])
            for url in urls:
                writer.writerow([url])

def categorize_by_type(urls):
    """Categorize URLs by their type"""
    categories = defaultdict(list)
    for url_data in urls:
        if isinstance(url_data, dict):
            url_type = url_data.get('type', 'unknown')
            categories[url_type].append(url_data)
    return dict(categories)

def extract_unique_urls(urls):
    """Extract just the URLs (no duplicates)"""
    unique_urls = set()
    for url_data in urls:
        if isinstance(url_data, dict):
            unique_urls.add(url_data['url'])
        else:
            unique_urls.add(url_data)
    return sorted(list(unique_urls))

def create_summary_report(data):
    """Create a comprehensive summary report"""
    report = f"""
DERIV.COM URL EXTRACTION SUMMARY REPORT
======================================
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Source page: {data['page_url']}

OVERVIEW
--------
Total URLs found: {data['total_urls_found']}
Internal URLs: {data['summary']['internal_count']}
External URLs: {data['summary']['external_count']}
Email links: {data['summary']['email_count']}
Phone links: {data['summary']['phone_count']}

INTERNAL URLS BY TYPE
-------------------
"""
    
    # Categorize internal URLs
    internal_by_type = categorize_by_type(data['internal_urls'])
    for url_type, urls in internal_by_type.items():
        report += f"{url_type.upper()}: {len(urls)} URLs\n"
    
    report += f"\nEXTERNAL URLS BY TYPE\n"
    report += f"-------------------\n"
    
    # Categorize external URLs
    external_by_type = categorize_by_type(data['external_urls'])
    for url_type, urls in external_by_type.items():
        report += f"{url_type.upper()}: {len(urls)} URLs\n"
    
    report += f"\nDOMAIN BREAKDOWN (External URLs)\n"
    report += f"-------------------------------\n"
    
    # Count domains for external URLs
    domain_count = defaultdict(int)
    for url_data in data['external_urls']:
        if isinstance(url_data, dict):
            domain = url_data.get('domain', 'unknown')
            domain_count[domain] += 1
    
    for domain, count in sorted(domain_count.items(), key=lambda x: x[1], reverse=True):
        report += f"{domain}: {count} URLs\n"
    
    return report

def main():
    print("🔄 Loading JSON data...")
    data = load_json_data('deriv_urls.json')
    
    # Create directory for separated URLs
    import os
    os.makedirs('separated_urls', exist_ok=True)
    
    print("📁 Separating URLs into categories...")
    
    # 1. Save Internal URLs
    print("  → Processing internal URLs...")
    save_urls_to_txt(data['internal_urls'], 'separated_urls/internal_urls.txt', 'INTERNAL URLS - DERIV.COM')
    save_urls_to_csv(data['internal_urls'], 'separated_urls/internal_urls.csv')
    
    # Save internal URLs by type
    internal_by_type = categorize_by_type(data['internal_urls'])
    for url_type, urls in internal_by_type.items():
        filename = f'separated_urls/internal_{url_type}_urls.txt'
        save_urls_to_txt(urls, filename, f'INTERNAL {url_type.upper()} URLS')
    
    # 2. Save External URLs
    print("  → Processing external URLs...")
    save_urls_to_txt(data['external_urls'], 'separated_urls/external_urls.txt', 'EXTERNAL URLS')
    save_urls_to_csv(data['external_urls'], 'separated_urls/external_urls.csv')
    
    # Save external URLs by type
    external_by_type = categorize_by_type(data['external_urls'])
    for url_type, urls in external_by_type.items():
        filename = f'separated_urls/external_{url_type}_urls.txt'
        save_urls_to_txt(urls, filename, f'EXTERNAL {url_type.upper()} URLS')
    
    # 3. Save Email Links (if any)
    if data['email_links']:
        print("  → Processing email links...")
        save_urls_to_txt(data['email_links'], 'separated_urls/email_links.txt', 'EMAIL LINKS')
        save_urls_to_csv(data['email_links'], 'separated_urls/email_links.csv')
    
    # 4. Save Phone Links (if any)
    if data['phone_links']:
        print("  → Processing phone links...")
        save_urls_to_txt(data['phone_links'], 'separated_urls/phone_links.txt', 'PHONE LINKS')
        save_urls_to_csv(data['phone_links'], 'separated_urls/phone_links.csv')
    
    # 5. Create unique URL lists
    print("  → Creating unique URL lists...")
    all_internal_urls = extract_unique_urls(data['internal_urls'])
    all_external_urls = extract_unique_urls(data['external_urls'])
    
    with open('separated_urls/all_internal_urls_simple.txt', 'w') as f:
        f.write("# All Internal URLs (Unique)\n")
        f.write("# " + "="*50 + "\n\n")
        for url in all_internal_urls:
            f.write(f"{url}\n")
    
    with open('separated_urls/all_external_urls_simple.txt', 'w') as f:
        f.write("# All External URLs (Unique)\n")
        f.write("# " + "="*50 + "\n\n")
        for url in all_external_urls:
            f.write(f"{url}\n")
    
    # 6. Create comprehensive summary
    print("  → Generating summary report...")
    summary = create_summary_report(data)
    with open('separated_urls/summary_report.txt', 'w') as f:
        f.write(summary)
    
    # 7. Create a master URL list
    print("  → Creating master URL list...")
    with open('separated_urls/all_urls_master.txt', 'w') as f:
        f.write("MASTER URL LIST - DERIV.COM\n")
        f.write("="*40 + "\n\n")
        f.write("INTERNAL URLS:\n")
        f.write("-"*20 + "\n")
        for url in all_internal_urls:
            f.write(f"{url}\n")
        f.write(f"\nEXTERNAL URLS:\n")
        f.write("-"*20 + "\n")
        for url in all_external_urls:
            f.write(f"{url}\n")
    
    print("\n✅ URL separation completed!")
    print(f"📊 Summary:")
    print(f"   • Internal URLs: {len(all_internal_urls)}")
    print(f"   • External URLs: {len(all_external_urls)}")
    print(f"   • Total unique URLs: {len(all_internal_urls) + len(all_external_urls)}")
    print(f"\n📁 All files saved in 'separated_urls/' directory")
    print("🔍 Check 'summary_report.txt' for detailed breakdown")

if __name__ == '__main__':
    main()


