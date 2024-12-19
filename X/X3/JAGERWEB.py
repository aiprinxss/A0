import requests

def test_requests():
    print("JAGERWEB")
    print("PROJECT X3")
    print("")
    url = input("ENTER URL IN FORM http://site.com: " )
    print("")

    response = requests.get(url)
    
    print(f'Status Code: {response.status_code}')
    print(f'Content: {response.text[:10000]}')
    print("")
    print("(c)JAGERCZECH CORP.")
test_requests()
