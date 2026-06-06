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

# WMO condition code mapping
WMO_CONDITIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Foggy",
    48: "Foggy",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with hail",
}


def get_condition_text(condition_code):
    """Convert WMO condition code to readable text."""
    try:
        return WMO_CONDITIONS.get(int(condition_code), "Unknown")
    except (ValueError, TypeError):
        return "Unknown"


def generate_farming_advisory(current_temp, humidity, wind_speed, precipitation_prob, condition_code):
    """Generate AI-based farming advisory based on weather conditions."""
    condition = get_condition_text(condition_code)
    
    advisories = []
    
    # Temperature advisory
    if current_temp > 30:
        advisories.append("⚠️ High temperature: Ensure adequate irrigation for crops. Increase watering frequency.")
    elif current_temp < 15:
        advisories.append("🌡️ Low temperature: Frost risk. Protect sensitive crops with mulching or covers.")
    else:
        advisories.append("✓ Optimal temperature for most crops.")
    
    # Humidity advisory
    if humidity > 80:
        advisories.append("💧 High humidity: Increased disease risk. Monitor for fungal infections. Ensure good ventilation.")
    elif humidity < 40:
        advisories.append("🏜️ Low humidity: High evaporation risk. Monitor soil moisture closely and increase irrigation.")
    else:
        advisories.append("✓ Humidity levels are favorable.")
    
    # Wind advisory
    if wind_speed > 15:
        advisories.append("💨 Strong winds: Risk of crop damage. Consider wind breaks or stakes for tall plants.")
    else:
        advisories.append("✓ Wind conditions are safe.")
    
    # Precipitation advisory
    if precipitation_prob > 70:
        advisories.append("🌧️ High rain probability: Prepare drainage systems. Avoid pesticide application before rain.")
    elif precipitation_prob < 20:
        advisories.append("☀️ Low rain probability: Plan irrigation accordingly. No rain protection needed.")
    
    return " ".join(advisories)


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
        api_data = response.json()
        
        # Transform API response to frontend format
        current = api_data.get("current", {})
        hourly = api_data.get("hourly", [])
        daily = api_data.get("daily", [])
        
        # Get current conditions
        current_temp = current.get("temperature")
        wind_speed = current.get("wind_speed", 0)
        condition_code = current.get("condition_code", 0)
        
        # Get humidity and feels_like from first hourly entry (current hour)
        current_humidity = 0
        current_feels_like = current_temp
        if hourly and len(hourly) > 0:
            current_humidity = hourly[0].get("humidity", 0)
            current_feels_like = hourly[0].get("feels_like", current_temp)
        
        # Get precipitation probability from first daily entry
        precipitation_prob = daily[0].get("precipitation_probability", 0) if daily else 0
        
        # Generate farming advisory
        ai_summary = generate_farming_advisory(
            current_temp, 
            current_humidity, 
            wind_speed, 
            precipitation_prob,
            condition_code
        )
        
        # Transform daily forecast
        forecast = []
        for day in daily:
            forecast.append({
                "date": day.get("date"),
                "temp_max": day.get("temp_max"),
                "temp_min": day.get("temp_min"),
                "condition": get_condition_text(day.get("condition_code")),
                "condition_code": day.get("condition_code"),
                "icon": day.get("icon"),
                "precipitation_sum": day.get("precipitation_sum", 0),
                "wind_max": day.get("wind_max", 0),
                "precipitation_probability": day.get("precipitation_probability", 0),
            })
        
        return jsonify({
            "searched_city": city.title() if city else DEFAULT_CITY,
            "current": {
                "temp": current_temp,
                "temperature": current_temp,
                "humidity": current_humidity,
                "feels_like": current_feels_like,
                "wind_speed": wind_speed,
                "condition": get_condition_text(condition_code),
                "condition_code": condition_code,
                "icon": current.get("icon"),
            },
            "forecast": forecast,
            "daily": forecast,
            "ai_summary": ai_summary,
            "location": {
                "name": city.title() if city else DEFAULT_CITY,
            },
        })
    except requests.exceptions.HTTPError as http_err:
        status_code = http_err.response.status_code if http_err.response is not None else 500
        message = http_err.response.text if http_err.response is not None else str(http_err)
        return jsonify({"error": f"Weather API error ({status_code}): {message}"}), status_code
    except requests.exceptions.RequestException as req_err:
        return jsonify({"error": f"Failed to fetch weather data: {req_err}"}), 500


if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=debug_mode,
        use_reloader=False,
    )
