import requests

URL = "https://gvwilson.github.io/tlscr/species.html"

response = requests.get(URL)
print(f"status code: {response.status_code}")
print("text:")
print(response.text)
