import requests
import json
import os
import signal
import sys
from datetime import datetime
from urllib.parse import urlparse, quote
import re
import socket

# Global variables for tracking data and file naming
data_list = []
filename = ""
processed_urls = set()
current_file_size = 0

def get_search_results(query):
    """Fetch search results based on the query."""
    url = f"https://www.bing.com/search?q={quote(query)}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print("Search results fetched successfully.")
    return response.text

def get_url_from_search_results(results):
    """Extract URLs from search results."""
    urls = re.findall(r'<a href="(https?://[^"]+)"', results)
    print(f"Extracted URLs: {urls}")
    return urls

def fetch_url_content(url):
    """Fetch content from the given URL and collect metadata."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        site_name = urlparse(url).hostname
        server_ip_address = socket.gethostbyname(site_name)  # Get the server's IP address
        date_accessed = datetime.now().isoformat()
        returned_value = response.text[:10000]
        print(f"Fetched content from {url}")
        return {
            "site_name": site_name,
            "server_ip_address": server_ip_address,
            "date_accessed": date_accessed,
            "returned_value": returned_value
        }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def sanitize_filename(filename):
    """Sanitize the filename to remove or replace invalid characters."""
    return re.sub(r'[^a-zA-Z0-9_-]', '_', filename)

def save_to_json_file(data, filename):
    """Save data to a JSON file, appending if the file already exists."""
    with open(filename, 'a') as file:
        file.write(json.dumps(data, indent=4))
        file.write(',\n')
    print(f"Data saved to {filename}")

def handler(signum, frame):
    global data_list
    global filename

    print("Stopping the program...")
    if data_list:
        save_to_json_file(data_list, filename)
    sys.exit(0)

def test_requests():
    """Main function to test HTTP GET requests and aggregate data."""
    global data_list
    global filename
    global processed_urls
    global current_file_size
    data_list = []
    current_file_size = 0

    signal.signal(signal.SIGINT, handler)
    query = input("Enter a hot word to search for: ")

    filename = f"jagerdata_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    while True:
        results = get_search_results(query)
        print(f"Raw search results: {results[:500]}")  # Print the first 500 characters of the results for debugging
        urls = get_url_from_search_results(results)
        print(f"URLs extracted: {urls}")

        new_urls = [url for url in urls if url not in processed_urls]
        processed_urls.update(new_urls)

        aggregated_data = [fetch_url_content(url) for url in new_urls if fetch_url_content(url)]
        print(f"Aggregated data: {aggregated_data}")

        for data in aggregated_data:
            if data:
                data_list.append(data)
                current_file_size += len(json.dumps(data, indent=4).encode('utf-8'))

            if current_file_size >= 1024 * 1024 * 1024:  # 1024 MB
                save_to_json_file(data_list, filename)
                data_list = []
                current_file_size = 0

        if data_list:
            save_to_json_file(data_list, filename)
        print(f"Current file size: {current_file_size} bytes")

if __name__ == "__main__":
    test_requests()
