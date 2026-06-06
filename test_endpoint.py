import requests
import json

response = requests.get('http://127.0.0.1:5000/weather', timeout=10)
data = response.json()

print("=== Full Response ===")
print(json.dumps(data, indent=2))
