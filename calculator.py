import requests
from flask import Flask, render_template, request
import ssl
import urllib3

# Disable SSL verification warnings for development (not for production!)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

# Weather code mapping (WMO codes to descriptions and emoji icons)
WEATHER_CODES = {
    0: ("Clear sky", "☀️"),
    1: ("Mainly clear", "🌤️"),
    2: ("Partly cloudy", "⛅"),
    3: ("Overcast", "☁️"),
    45: ("Foggy", "🌫️"),
    48: ("Foggy", "🌫️"),
    51: ("Light drizzle", "🌧️"),
    53: ("Moderate drizzle", "🌧️"),
    55: ("Dense drizzle", "🌧️"),
    61: ("Slight rain", "🌧️"),
    63: ("Moderate rain", "🌧️"),
    65: ("Heavy rain", "⛈️"),
    71: ("Slight snow", "❄️"),
    73: ("Moderate snow", "❄️"),
    75: ("Heavy snow", "❄️"),
    77: ("Snow grains", "❄️"),
    80: ("Slight rain showers", "🌧️"),
    81: ("Moderate rain showers", "🌧️"),
    82: ("Violent rain showers", "⛈️"),
    85: ("Slight snow showers", "❄️"),
    86: ("Heavy snow showers", "❄️"),
    95: ("Thunderstorm", "⛈️"),
    96: ("Thunderstorm with hail", "⛈️"),
    99: ("Thunderstorm with hail", "⛈️"),
}


def get_city_coordinates(city_name):
    """Fetch latitude and longitude for a city using Open-Meteo geocoding API."""
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
        response = requests.get(url, params=params, timeout=5, verify=False)
        response.raise_for_status()
        
        data = response.json()
        if not data.get("results"):
            return None
        
        result = data["results"][0]
        return {
            "name": result.get("name"),
            "country": result.get("country"),
            "latitude": result.get("latitude"),
            "longitude": result.get("longitude"),
        }
    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None


def get_forecast(latitude, longitude, unit="fahrenheit"):
    """Fetch 5-day daily forecast from Open-Meteo API."""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "daily": "temperature_2m_max,temperature_2m_min,weather_code",
            "temperature_unit": unit,
            "forecast_days": 6,
            "timezone": "auto",
        }
        response = requests.get(url, params=params, timeout=5, verify=False)
        response.raise_for_status()

        data = response.json()
        daily = data.get("daily", {})
        dates = daily.get("time", [])[1:6]
        max_temps = daily.get("temperature_2m_max", [])[1:6]
        min_temps = daily.get("temperature_2m_min", [])[1:6]
        codes = daily.get("weather_code", [])[1:6]

        forecast = []
        for i, date in enumerate(dates):
            from datetime import datetime
            day_name = datetime.strptime(date, "%Y-%m-%d").strftime("%a")
            code = codes[i] if i < len(codes) else 0
            condition, icon = WEATHER_CODES.get(code, ("Unknown", "❓"))
            forecast.append({
                "day": day_name,
                "icon": icon,
                "condition": condition,
                "high": max_temps[i] if i < len(max_temps) else None,
                "low": min_temps[i] if i < len(min_temps) else None,
            })
        return forecast
    except requests.exceptions.RequestException:
        return []
    except Exception:
        return []


def get_weather(latitude, longitude, unit="fahrenheit"):
    """Fetch current weather data from Open-Meteo API."""
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,uv_index",
            "temperature_unit": unit,
        }
        response = requests.get(url, params=params, timeout=5, verify=False)
        response.raise_for_status()
        
        data = response.json()
        current = data.get("current", {})
        
        weather_code = current.get("weather_code", 0)
        condition, icon = WEATHER_CODES.get(weather_code, ("Unknown", "❓"))
        
        return {
            "temperature": current.get("temperature_2m"),
            "condition": condition,
            "icon": icon,
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "feels_like": current.get("apparent_temperature"),
            "uv_index": current.get("uv_index"),
        }
    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None


@app.route("/", methods=["GET", "POST"])
def index():
    """Handle home page and form submission."""
    weather_data = None
    city_info = None
    error = None
    forecast = []
    unit = request.form.get("unit", "fahrenheit")
    unit_symbol = "F" if unit == "fahrenheit" else "C"

    if request.method == "POST":
        city_name = request.form.get("city", "").strip()
        
        if not city_name:
            error = "Please enter a city name."
        else:
            # Get city coordinates
            city_info = get_city_coordinates(city_name)
            
            if not city_info:
                error = f"City '{city_name}' not found. Please try again."
            else:
                # Get weather data
                weather_data = get_weather(city_info["latitude"], city_info["longitude"], unit)
                forecast = get_forecast(city_info["latitude"], city_info["longitude"], unit)
                
                if not weather_data:
                    error = "Unable to fetch weather data. Please try again later."
    
    return render_template(
        "weather.html",
        weather_data=weather_data,
        city_info=city_info,
        error=error,
        forecast=forecast,
        unit=unit,
        unit_symbol=unit_symbol,
    )


if __name__ == "__main__":
    app.run(debug=True)
