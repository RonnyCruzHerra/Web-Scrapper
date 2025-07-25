import requests

resp = requests.post(
    "http://localhost:5050/api/scrape-amazon-dynamic",
    json={"query": "monitor", "pages": 1}
)
print(resp.json())