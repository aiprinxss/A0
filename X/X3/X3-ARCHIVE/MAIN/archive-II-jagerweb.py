import requests

def get_url_from_user():
    """Prompt user to enter a URL."""
    print("JAGERWEB")
    print("PROJECT X3")
    print("")
    url = input("ENTER URL IN FORM http://site.com: " )
    print("")
    return url

def fetch_url_content(url):
    """Fetch content from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def display_response(response):
    """Display the response status code and content."""
    if response:
        print(f'Status Code: {response.status_code}')
        print(f'Content: {response.text[:10000]}')  # Limit output to 10,000 characters
    print("")
    print("(c)JAGERCZECH CORP.")

def test_requests():
    """Main function to test HTTP GET requests."""
    url = get_url_from_user()
    response = fetch_url_content(url)
    display_response(response)

if __name__ == "__main__":
    test_requests()
