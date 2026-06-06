import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

url = "https://api.weather-ai.co/v1/weather"
headers = {"Authorization": f"Bearer {api_key}"}
params = {
    "lat": -1.2921,
    "lon": 36.8219,
    "days": 7,
    "ai": "true",
    "units": "metric",
}

response = requests.get(url, headers=headers, params=params, timeout=15)
data = response.json()

print("=== FULL API RESPONSE ===")
print(json.dumps(data, indent=2))
