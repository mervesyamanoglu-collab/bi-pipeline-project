# BI Pipeline Project – Weather Data Analytics for 8 European Cities

This project is an end-to-end Business Intelligence (BI) pipeline built with Python, MongoDB, Docker, and Power BI. It collects weather data for 8 European cities from the OpenWeatherMap API, cleans and transforms the data, stores it in MongoDB, orchestrates the workflow automatically, and visualizes the results in Power BI.

## Business Case

Logistics and operational decisions are directly affected by weather conditions.  
The goal of this project is to monitor temperature, humidity, and wind conditions across multiple cities in near real time and turn raw API responses into structured, analysis-ready datasets for reporting and decision-making.

## Project Workflow

The pipeline consists of five main stages:

1. **Data Collection**
2. **Data Cleaning and Transformation**
3. **Data Storage**
4. **Pipeline Orchestration**
5. **Data Visualization**

In addition, the project includes a **bonus machine learning component** and **Docker-based containerization**.

## Project Structure

```text
BI-PROJECT/
│
├── 1_data_collection.py
├── 2_data_cleaning.py
├── 2b_forecast_transform.py
├── 3_data_storage.py
├── 4_pipeline_orchestrator.py
├── 5_machine_learning.py
├── Dockerfile
├── requirements.txt
├── pipeline_log.txt
├── Dashboard.pbix
├── data/
│   ├── raw/
│   │   ├── current_weather.json
│   │   └── forecast_weather.json
│   └── processed/
│       ├── current_weather_clean.csv
│       ├── forecast_weather_clean.csv
│       └── daily_forecast_agg.csv
```

## Pipeline Steps

### 1. Data Collection – `1_data_collection.py`

This script fetches:
- current weather data for 8 European cities
- 5-day forecast data from the OpenWeatherMap API

The API key is stored in a `.env` file instead of being hard-coded in the source code.

### 2. Data Cleaning – `2_data_cleaning.py`

This script processes the current weather dataset:
- converts raw JSON into a pandas DataFrame
- removes null values
- fixes incorrect country codes returned by the API using manual mapping
- exports the cleaned dataset as:

```text
data/processed/current_weather_clean.csv
```

### 3. Forecast Transformation – `2b_forecast_transform.py`

This script processes the forecast dataset:
- flattens nested JSON into a tabular structure
- produces a 320-row forecast DataFrame
- performs daily aggregation for each city
- calculates daily minimum, maximum, and average values for:
  - temperature
  - humidity
  - wind speed

Outputs:
```text
data/processed/forecast_weather_clean.csv
data/processed/daily_forecast_agg.csv
```

### 4. Data Storage – `3_data_storage.py`

This script loads the processed CSV files into MongoDB and creates three collections:

- `current_weather` → 8 records
- `forecast_weather` → 320 records
- `daily_forecast_agg` → 40 records

The stored data can be verified through MongoDB Compass.

### 5. Orchestration – `4_pipeline_orchestrator.py`

This script automates the pipeline execution by running the major steps in sequence.

Features:
- logs execution results into `pipeline_log.txt`
- continues execution even if one step fails
- sends automatic email notifications via SMTP when an error occurs

### 6. Machine Learning – `5_machine_learning.py`

As a bonus component, the project includes a simple **Linear Regression** model built with scikit-learn.

- **Inputs:** humidity and wind speed
- **Target:** temperature

The model is trained using an 80/20 train-test split and achieved:

- **R² = 0.70**
- **MSE = 8.49**

This means the model explains about 70% of the variance in temperature using the selected weather features.

### 7. Power BI Dashboard

The Power BI dashboard visualizes:
- current weather metrics
- forecast trends
- city-based comparisons
- average temperature, humidity, and wind speed

Dashboard files:
- `Dashboard.pbix`
- `Dashboard - Kopya.pbix`

## Technologies Used

- **Python**
- **pandas**
- **scikit-learn**
- **MongoDB**
- **MongoDB Compass**
- **Docker**
- **Power BI**
- **SMTP / Gmail notification system**

## Requirements

All Python dependencies are listed in `requirements.txt`.

Install them with:

```bash
pip install -r requirements.txt
```

This ensures the same environment can be recreated on another machine.

## How to Run the Project

### Run each step manually

```bash
python 1_data_collection.py
python 2_data_cleaning.py
python 2b_forecast_transform.py
python 3_data_storage.py
python 4_pipeline_orchestrator.py
python 5_machine_learning.py
```

### Run with Docker

Build the image:

```bash
docker build -t bi_project .
```

List Docker images:

```bash
docker images
```

Run the container:

```bash
docker run --env-file .env bi_project
```

## Environment Variables

Sensitive credentials are not written directly in the code.  
They are stored in a `.env` file.

Example:

```env
OPENWEATHER_API_KEY=your_api_key
MONGO_URI=your_mongo_connection_string
EMAIL_USER=your_email
EMAIL_PASS=your_email_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

## Key Features

- End-to-end BI pipeline
- API-based real-world data collection
- Separate cleaning logic for current and forecast data
- MongoDB integration
- Automated orchestration
- Error logging and email notification
- Docker containerization
- Power BI dashboarding
- Bonus machine learning model

## Author

**Merve S. Yamanoglu**
