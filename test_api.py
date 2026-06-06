import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
print(f"API Key: {api_key[:20]}...")

# Test the weather endpoint
url = "https://api.weather-ai.co/v1/weather"
headers = {"Authorization": f"Bearer {api_key}"}
params = {
    "lat": -1.2921,
    "lon": 36.8219,
    "days": 7,
    "ai": "true",
    "units": "metric",
}

try:
    response = requests.get(url, headers=headers, params=params, timeout=15)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Keys in response: {list(data.keys())}")
        if "current" in data:
            print(f"Current temp: {data['current'].get('temp')}°C")
        if "forecast" in data:
            print(f"Forecast days: {len(data['forecast'])}")
    else:
        print(f"Error: {response.text[:200]}")
except Exception as e:
    print(f"Request failed: {e}")
