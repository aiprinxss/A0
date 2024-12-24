import requests
import json
from datetime import datetime
from urllib.parse import urlparse
import re

def get_url_from_user():
    """Prompt user to enter a URL."""
    print("JAGERWEB")
    print("PROJECT X3")
    print("")
    url = input("ENTER URL IN FORM http://site.com: " )
    print("")
    return url

def fetch_url_content(url):
    """Fetch content from the given URL and collect metadata."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        site_name = urlparse(url).hostname
        ip_address = requests.get('https://api.ipify.org').text  # Get the public IP address
        date_accessed = datetime.now().isoformat()
        returned_value = response.text[:10000]  # Limit to first 10,000 characters
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

def aggregate_data(urls):
    """Aggregate data from multiple URLs."""
    aggregated_data = []
    for url in urls:
        content = fetch_url_content(url)
        if content:
            aggregated_data.append(content)
    return aggregated_data

def display_aggregated_data(aggregated_data):
    """Display the aggregated data in JSON format."""
    aggregated_json = json.dumps(aggregated_data, indent=4)
    print(aggregated_json)
    return aggregated_json

def save_to_json_file(aggregated_data):
    """Save the aggregated data to a JSON file with a unique name."""
    for data in aggregated_data:
        site_name = sanitize_filename(data['site_name'])
        filename = f"{site_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Aggregated data saved to {filename}")

def test_requests():
    """Main function to test HTTP GET requests and aggregate data."""
    urls = []
    for _ in range(3):  # Prompt user for 3 URLs (or any number you prefer)
        urls.append(get_url_from_user())
    
    aggregated_data = aggregate_data(urls)
    aggregated_json = display_aggregated_data(aggregated_data)
    save_to_json_file(aggregated_data)

if __name__ == "__main__":
    test_requests()
