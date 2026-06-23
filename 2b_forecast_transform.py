import pandas as pd
import json
import os

print("Starting forecast data transformation...")

forecast_path = os.path.join("data", "raw", "forecast_weather.json")

try:
    with open(forecast_path, "r", encoding="utf-8") as f:
        forecast_raw = json.load(f)
    print("Successfully loaded forecast_weather.json")
except FileNotFoundError:
    print("ERROR: Run 1_data_collection.py first.")
    exit()

# Flatten nested JSON
rows = []
for entry in forecast_raw:
    city_name = entry["city"]["name"]
    country   = entry["city"]["country"]
    for slot in entry["list"]:
        rows.append({
            "city":             city_name,
            "country":          country,
            "forecast_dt":      pd.to_datetime(slot["dt"], unit="s"),
            "dt_txt":           slot.get("dt_txt"),
            "temperature_c":    slot["main"]["temp"],
            "humidity_percent": slot["main"]["humidity"],
            "condition":        slot["weather"][0]["main"] if slot.get("weather") else None,
            "wind_speed_m_s":   slot["wind"]["speed"],
        })

df_forecast = pd.DataFrame(rows).dropna()
print(f"Extracted {len(df_forecast)} rows across {df_forecast['city'].nunique()} cities.")

# Daily aggregation
df_forecast["date"] = df_forecast["forecast_dt"].dt.date

df_daily = (
    df_forecast
    .groupby(["city", "date"])
    .agg(
        temp_min     = ("temperature_c",    "min"),
        temp_max     = ("temperature_c",    "max"),
        temp_avg     = ("temperature_c",    "mean"),
        humidity_avg = ("humidity_percent", "mean"),
        wind_avg     = ("wind_speed_m_s",   "mean"),
    )
    .reset_index()
)

os.makedirs(os.path.join("data", "processed"), exist_ok=True)
df_forecast.to_csv(os.path.join("data", "processed", "forecast_weather_clean.csv"), index=False)
df_daily.to_csv(os.path.join("data", "processed", "daily_forecast_agg.csv"), index=False)

print(f"Saved forecast_weather_clean.csv ({len(df_forecast)} rows)")
print(f"Saved daily_forecast_agg.csv ({len(df_daily)} rows)")
print("Forecast transformation complete!")