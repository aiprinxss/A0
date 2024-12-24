import requests
import json
import os
import signal
import sys
from datetime import datetime
from urllib.parse import urlparse, quote
import re

def get_search_results(query):
    """Fetch search results based on the query."""
    url = f"https://duckduckgo.com/html?q={quote(query)}"
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def get_url_from_search_results(results):
    """Extract URLs from search results."""
    urls = re.findall(r'<a rel="nofollow" class="result__a" href="([^"]+)"', results)
    return [url for url in urls if url.startswith('http')]

def fetch_url_content(url):
    """Fetch content from the given URL and collect metadata."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        site_name = urlparse(url).hostname
        ip_address = requests.get('https://api.ipify.org').text
        date_accessed = datetime.now().isoformat()
        returned_value = response.text[:10000]
        return {
            "site_name": site_name,
            "ip_address": ip_address,
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

def handler(signum, frame):
    print("Stopping the program...")
    sys.exit(0)

def test_requests():
    """Main function to test HTTP GET requests and aggregate data."""
    signal.signal(signal.SIGINT, handler)
    query = input("Enter a hot word to search for: ")

    while True:
        results = get_search_results(query)
        urls = get_url_from_search_results(results)
        aggregated_data = [fetch_url_content(url) for url in urls if fetch_url_content(url)]

        filename = f"aggregated_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        current_file_size = 0
        data_list = []

        for data in aggregated_data:
            if data:
                data_list.append(data)
                current_file_size += len(json.dumps(data, indent=4).encode('utf-8'))

            if current_file_size >= 1024 * 1024 * 1024:
                save_to_json_file(data_list, filename)
                data_list = []
                current_file_size = 0
                filename = f"aggregated_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        if data_list:
            save_to_json_file(data_list, filename)

if __name__ == "__main__":
    test_requests()
