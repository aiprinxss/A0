import requests
import os
import signal
import sys
import sqlite3
from datetime import datetime
from urllib.parse import urlparse, quote
import re
import socket

# Global variables for tracking data and database connection
processed_urls = set()
conn = sqlite3.connect('jagerdata.db')
cur = conn.cursor()

def initialize_database():
    """Initialize the SQLite database and create the necessary table."""
    cur.execute('''
        CREATE TABLE IF NOT EXISTS data (
            site_name TEXT,
            server_ip_address TEXT,
            date_accessed TEXT,
            returned_value TEXT
        )
    ''')
    conn.commit()
    print("Database initialized and table created.")

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

def save_to_database(data):
    """Save data to the SQLite database."""
    cur.execute('''
        INSERT INTO data (site_name, server_ip_address, date_accessed, returned_value)
        VALUES (?, ?, ?, ?)
    ''', (data['site_name'], data['server_ip_address'], data['date_accessed'], data['returned_value']))
    conn.commit()
    print("Data saved to the database.")

def handler(signum, frame):
    print("Stopping the program...")
    conn.close()
    sys.exit(0)

def test_requests():
    """Main function to test HTTP GET requests and aggregate data."""
    global processed_urls

    signal.signal(signal.SIGINT, handler)
    query = input("Enter a hot word to search for: ")

    initialize_database()

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
                save_to_database(data)

if __name__ == "__main__":
    test_requests()
