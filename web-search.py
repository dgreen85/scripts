#Primarily created with OpenAI's ChatGPT 4o
#This script searches a .csv full of URLs for a specific phrase within specific IDs or Classes of a webpage. Output provides csv with url, html line and surrounding text for each mention of the phrase within the body content of that website. 

import csv
import requests
import time
from bs4 import BeautifulSoup

# Function to fetch webpage content
def fetch_webpage_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

# Function to search for the phrase in main content with given ids/classes
def search_phrase_in_content(html_content, phrase, ids_classes, url):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    id_class_found = False

    # Check each id/class for main content
    for id_class in ids_classes:
        try:
            element = soup.find(id=id_class) or soup.find(class_=id_class)
            if element:
                id_class_found = True
                text = element.get_text()
                start = 0
                while (index := text.find(phrase, start)) != -1:
                    start = index + len(phrase)
                    context = text[max(0, index-15):index+len(phrase)+15]
                    results.append((index, context))
                break
        except Exception as e:
            print(f"Error processing id/class '{id_class}' in {url}: {e}")

    if not id_class_found:
        print(f"No main content id/class found in {url}")

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
        csvwriter.writerow(['URL', 'HTML Line', 'Context'])
        for url, occurrences in results.items():
            for line, context in occurrences:
                csvwriter.writerow([url, line, context])

# Main function
def main(input_csv, output_csv, phrase, ids_classes):
    urls = read_urls_from_csv(input_csv)
    results = {}
    for url in urls:
        try:
            html_content = fetch_webpage_content(url)
            if html_content:
                occurrences = search_phrase_in_content(html_content, phrase, ids_classes, url)
                if occurrences:
                    results[url] = occurrences
                    print(f"{url}: Phrase found {len(occurrences)} times.")
                else:
                    print(f"{url}: Phrase not found.")
            else:
                print(f"{url}: Error fetching content.")
        except Exception as e:
            print(f"Error processing {url}: {e}")

        time.sleep(1)  # 1 second delay between requests
    
    write_results_to_csv(output_csv, results)
    print(f"Results written to {output_csv}")




# Inputs
input_csv = 'url-list.csv'
output_csv = 'output_results.csv'
phrase = 'phrase'  # Replace with the phrase you are searching for
ids_classes = ['content', 'page-content', 'post', 'resources', 'shows', 'news', 'testimonials', 'events']  # Replace with your actual ids and classes
main(input_csv, output_csv, phrase, ids_classes)
