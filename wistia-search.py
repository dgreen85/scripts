import csv
import requests
import time
from bs4 import BeautifulSoup
import re

# Function to fetch webpage content
def fetch_webpage_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to search for Wistia video URLs and extract Wistia IDs
def search_wistia_urls(html_content, url):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    
    # Regex for Wistia URLs
    wistia_regex = r'https://fast\.wistia\.com/embed/medias/([a-zA-Z0-9]+)\.jsonp'
    
    # Search for matches in all script tags
    script_tags = soup.find_all('script', src=True)
    for script in script_tags:
        src = script['src']
        match = re.search(wistia_regex, src)
        if match:
            wistia_id = match.group(1)
            results.append(wistia_id)
    
    return results

# Read URLs from CSV
def read_urls_from_csv(file_path):
    urls = []
    with open(file_path, mode='r', newline='') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row if present
        for row in csvreader:
            urls.append(row[0])  # Assumes URL is in the first column
    return urls

# Write results to output CSV
def write_results_to_csv(file_path, results):
    with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['URL', 'Wistia ID'])
        for url, wistia_ids in results.items():
            for wistia_id in wistia_ids:
                csvwriter.writerow([url, wistia_id])

# Main function
def main(input_csv, output_csv):
    urls = read_urls_from_csv(input_csv)
    results = {}
    for url in urls:
        try:
            html_content = fetch_webpage_content(url)
            if html_content:
                wistia_ids = search_wistia_urls(html_content, url)
                if wistia_ids:
                    results[url] = wistia_ids
                    print(f"{url}: Found {len(wistia_ids)} Wistia IDs.")
                else:
                    print(f"{url}: No Wistia videos found.")
            else:
                print(f"{url}: Error fetching content.")
        except Exception as e:
            print(f"Error processing {url}: {e}")

        time.sleep(1)  # 1 second delay between requests
    
    write_results_to_csv(output_csv, results)
    print(f"Results written to {output_csv}")

# Inputs
input_csv = 'url-list.csv'
output_csv = 'wistia_results.csv'

main(input_csv, output_csv)
