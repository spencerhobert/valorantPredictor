import requests

r = requests.get("http://localhost:8000/scraper/")

print(r.text)