import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

CITIES = ["Munich", "Berlin", "Paris", "London", "Rome", "Madrid", "Vienna", "Amsterdam"]
BASE_URL_CURRENT = "http://api.openweathermap.org/data/2.5/weather"
BASE_URL_FORECAST = "http://api.openweathermap.org/data/2.5/forecast"

current_weather_raw = []
forecast_weather_raw = []

print("Starting data collection process...")

for city in CITIES:
    params = {"q": city, "appid": API_KEY, "units": "metric"}
    
    # 1. Fetch Current Weather Data
    response_current = requests.get(BASE_URL_CURRENT, params=params)
    if response_current.status_code == 200:
        current_weather_raw.append(response_current.json())
        print(f"Successfully fetched current weather data for {city}.")
    else:
        print(f"ERROR: Could not fetch current weather for {city}. (Code: {response_current.status_code})")
    
    # 2. Fetch 5-Day Forecast Data
    response_forecast = requests.get(BASE_URL_FORECAST, params=params)
    if response_forecast.status_code == 200:
        forecast_weather_raw.append(response_forecast.json())
        print(f"Successfully fetched forecast data for {city}.")
    else:
        print(f"ERROR: Could not fetch forecast for {city}. (Code: {response_forecast.status_code})")

# Create directory if it doesn't exist
os.makedirs(os.path.join("data", "raw"), exist_ok=True)

# Save raw data as JSON files
with open(os.path.join("data", "raw", "current_weather.json"), "w", encoding="utf-8") as f:
    json.dump(current_weather_raw, f, indent=4)

with open(os.path.join("data", "raw", "forecast_weather.json"), "w", encoding="utf-8") as f:
    json.dump(forecast_weather_raw, f, indent=4)

print("\nData collection completed! Raw data saved to 'data/raw' as JSON files.")