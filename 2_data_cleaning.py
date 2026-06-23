import pandas as pd
import json
import os

print("Starting data cleaning and preparation process...")

# 1. Load Raw Data
current_path = os.path.join("data", "raw", "current_weather.json")

try:
    with open(current_path, "r", encoding="utf-8") as f:
        current_raw = json.load(f)
    print("Successfully loaded raw JSON data.")
except FileNotFoundError:
    print("ERROR: Raw data files not found. Please run 1_data_collection.py first.")
    exit()

# 2. Extract and Transform Data
processed_data = []

for item in current_raw:
    processed_data.append({
        "city": item.get("name"),
        "country": item.get("sys", {}).get("country"),
        "temperature_c": item.get("main", {}).get("temp"),
        "humidity_percent": item.get("main", {}).get("humidity"),
        "condition": item["weather"][0]["main"] if item.get("weather") else None,
        "wind_speed_m_s": item.get("wind", {}).get("speed"),
        # Convert Unix timestamp to readable Datetime
        "timestamp": pd.to_datetime(item.get("dt"), unit='s')
    })

# 3. Create Pandas DataFrame
df = pd.DataFrame(processed_data)

# 4. Handle Missing or Inconsistent Data (Drop N/A)
initial_rows = len(df)
df = df.dropna()
final_rows = len(df)
print(f"Data cleaning check: Dropped {initial_rows - final_rows} rows with missing values.")


# Fix incorrect country codes from API mismatches  ← BURAYA EKLE
country_fix = {
    "Rome": "IT", "Munich": "DE", "Berlin": "DE",
    "Paris": "FR", "London": "GB", "Vienna": "AT", "Amsterdam": "NL", "Madrid": "ES"
}
df["country"] = df["city"].map(country_fix).fillna(df["country"])
print("Country codes verified and corrected.")



# 5. Save Processed Data
os.makedirs(os.path.join("data", "processed"), exist_ok=True)
processed_save_path = os.path.join("data", "processed", "current_weather_clean.csv")

df.to_csv(processed_save_path, index=False)
print(f"\nData preparation completed! Clean dataset saved to: {processed_save_path}")

# Display the first few rows to verify
print("\n--- Cleaned Data Preview ---")
print(df.head())