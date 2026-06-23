import pandas as pd
import os
from pymongo import MongoClient
from dotenv import load_dotenv

print("Starting data storage process...")

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")

# ── Load all processed files ───────────────────────────────────────────────
files = {
    "current_weather":   os.path.join("data", "processed", "current_weather_clean.csv"),
    "forecast_weather":  os.path.join("data", "processed", "forecast_weather_clean.csv"),
    "daily_forecast_agg": os.path.join("data", "processed", "daily_forecast_agg.csv"),
}

dataframes = {}
for name, path in files.items():
    try:
        dataframes[name] = pd.read_csv(path)
        print(f"Loaded {name} ({len(dataframes[name])} rows)")
    except FileNotFoundError:
        print(f"ERROR: {path} not found. Run cleaning scripts first.")
        exit()

# ── Connect to MongoDB ─────────────────────────────────────────────────────
try:
    client = MongoClient(MONGO_URI)
    db = client["weather_logistics_db"]

    for collection_name, df in dataframes.items():
        collection = db[collection_name]
        collection.delete_many({})  # Avoid duplicates on re-run
        records = df.to_dict("records")
        collection.insert_many(records)
        print(f"Inserted {len(records)} records → collection: {collection_name}")

    print("\nDatabase: weather_logistics_db")
    print("Collections: current_weather | forecast_weather | daily_forecast_agg")

except Exception as e:
    print(f"ERROR: Database operation failed. Details: {e}")

print("\nData storage phase completed!")