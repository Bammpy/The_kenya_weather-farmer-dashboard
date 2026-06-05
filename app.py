from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_BASE_URL = "https://api.weather-ai.co/v1"
API_KEY = os.getenv("API_KEY")
DEFAULT_CITY = "Nairobi"
CITY_COORDS = {
    "nairobi": {"lat": -1.2921, "lon": 36.8219},
    "kisumu": {"lat": -0.0917, "lon": 34.7680},
    "eldoret": {"lat": 0.5143, "lon": 35.2699},
    "nakuru": {"lat": -0.3031, "lon": 36.0800},
    "mombasa": {"lat": -4.0435, "lon": 39.6682},
    "kakamega": {"lat": 0.2827, "lon": 34.7519},
    "nyeri": {"lat": -0.4210, "lon": 36.9510},
    "meru": {"lat": 0.0514, "lon": 37.6459},
    "kitale": {"lat": 1.0190, "lon": 34.9990},
    "embu": {"lat": -0.5390, "lon": 37.4570},
}


def get_city_coords(city_name: str):
    return CITY_COORDS.get(city_name.lower(), CITY_COORDS[DEFAULT_CITY.lower()])


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/weather', methods=['GET'])
def get_weather():
    if not API_KEY or not API_KEY.startswith("wai_"):
        return jsonify({
            "error": "Invalid or missing API key. Please set API_KEY in your .env or deployment environment."
        }), 401

    city = request.args.get('city', '').strip()
    city_key = city.lower() if city else DEFAULT_CITY.lower()
    coords = get_city_coords(city_key)

    headers = {"Authorization": f"Bearer {API_KEY}"}
    params = {
        "lat": coords["lat"],
        "lon": coords["lon"],
        "days": 7,
        "ai": "true",
        "units": "metric",
    }

    try:
        response = requests.get(f"{API_BASE_URL}/weather", headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        data["searched_city"] = city.title() if city else DEFAULT_CITY
        return jsonify(data)
    except requests.exceptions.HTTPError as http_err:
        status_code = http_err.response.status_code if http_err.response is not None else 500
        message = http_err.response.text if http_err.response is not None else str(http_err)
        return jsonify({"error": f"Weather API error ({status_code}): {message}"}), status_code
    except requests.exceptions.RequestException as req_err:
        return jsonify({"error": f"Failed to fetch weather data: {req_err}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
