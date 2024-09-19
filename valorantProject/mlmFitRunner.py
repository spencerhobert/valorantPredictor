import requests

r = requests.get("http://localhost:8000/mlm/fit")

print(r.text)