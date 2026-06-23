# BI Pipeline Project – Weather Data for 8 European Cities

Bu projede 8 Avrupa şehrinin hava durumu verisini OpenWeatherMap API'den
toplayarak uçtan uca bir Business Intelligence (BI) pipeline kurdum.

## Business Case

Lojistik ve operasyonel kararlar hava koşullarından doğrudan etkilenir.
Amaç: 8 şehir için anlık ve 5 günlük hava tahminlerini takip ederek
rüzgar, nem ve sıcaklık gibi metrikleri merkezi bir BI pipeline ile izlemek.

## Pipeline Adımları

1. **Data Collection – `1_data_collection.py`**
   - OpenWeatherMap API'den 8 şehir için:
     - Anlık hava durumu (`current_weather.json`)
     - 5 günlük / 3 saatlik tahmin verisi (`forecast_weather.json`)
   - API key, `.env` dosyasında tutuluyor, kodda hard-coded değil.

2. **Data Cleaning – `2_data_cleaning.py` & `2b_forecast_transform.py`**
   - Anlık hava verisi:
     - Ham JSON → pandas DataFrame
     - Null değerler temizleniyor
     - API'nin hatalı ülke kodları (ör. Rome için GB) manuel mapping ile IT olarak düzeltiliyor
     - Çıktı: `data/processed/current_weather_clean.csv`
   - Tahmin verisi:
     - İç içe JSON yapı düzleştiriliyor (nested list → flat tablo)
     - 320 satırlık forecast DataFrame oluşturuluyor
     - Günlük bazda aggregation:
       - Her şehir + her gün için min / max / mean sıcaklık, nem, rüzgar
     - Çıktılar:
       - `data/processed/forecast_weather_clean.csv`
       - `data/processed/daily_forecast_agg.csv`

3. **Data Storage – `3_data_storage.py`**
   - Temizlenmiş CSV'ler MongoDB'ye yazılıyor:
     - `current_weather` (8 kayıt)
     - `forecast_weather` (320 kayıt)
     - `daily_forecast_agg` (40 kayıt)
   - MongoDB Compass ile veriler görsel olarak doğrulanabiliyor.

4. **Orchestration – `4_pipeline_orchestrator.py`**
   - Tüm adımları otomatik sırayla çalıştıran basit bir orchestrator:
     1. Collection
     2. Cleaning
     3. Storage
   - Her adımın sonucu `pipeline_log.txt` içinde loglanıyor.
   - Hata durumunda:
     - Pipeline durmuyor, hatayı kaydedip devam ediyor
     - SMTP üzerinden Gmail ile otomatik email bildirimi gönderiyor.

5. **Machine Learning – `5_machine_learning.py`**
   - Bonus olarak basit bir Linear Regression modeli:
     - Girdi: Nem (`humidity`) ve rüzgar hızı (`wind_speed`)
     - Çıktı: Sıcaklık (`temperature`)
   - scikit-learn kullanılarak:
     - Train–test split (%80 / %20)
     - Model eğitimi ve değerlendirme
   - Performans:
     - R² ≈ 0.70
     - Model, sıcaklık değişkenliğinin yaklaşık %70'ini açıklıyor.

6. **Visualization – Power BI Dashboard**
   - `Dashboard.pbix` dosyasında:
     - 8 şehir için anlık ve tahmin verileri
     - Ortalama sıcaklık, nem ve rüzgar hızları
     - Şehir bazında karşılaştırmalar ve özet metrikler
   - Kullanılan veri kaynakları:
     - `current_weather_clean.csv`
     - `daily_forecast_agg.csv`

## Docker

Projeyi container içinde çalıştırmak için:

```bash
docker build -t bi_project .
docker images
docker run --env-file .env bi_project
```

- `Dockerfile` Python imajını (3.12-slim) kullanır.
- `requirements.txt` tüm bağımlılıkları sabit versiyonları ile içerir.
- `.env` dosyası container'a `--env-file` ile geçirilir, ama GitHub'a eklenmez.

## Teknolojiler

- Python, pandas, scikit-learn
- MongoDB
- Docker
- Power BI
- SMTP (Gmail) ile notification sistemi

## Çalıştırma

```bash
# 1. Sanal ortam (isteğe bağlı)
python -m venv venv
venv\Scripts\activate  # Windows

# 2. Bağımlılıkları yükle
pip install -r requirements.txt

# 3. Pipeline'ı manuel çalıştır
python 1_data_collection.py
python 2_data_cleaning.py
python 2b_forecast_transform.py
python 3_data_storage.py

# 4. Orchestrator ile otomatik çalıştır
python 4_pipeline_orchestrator.py

# 5. Machine learning modeli
python 5_machine_learning.py
```

`.env` dosyasında aşağıdaki değişkenler tanımlanmalıdır (örnek):

```env
OPENWEATHER_API_KEY=...
MONGO_URI=...
SMTP_HOST=...
SMTP_PORT=...
EMAIL_USER=...
EMAIL_PASS=...
```

---

Bunu `README.md` olarak ekleyip commit/push yaparsan repo sunumunla birebir uyumlu, çok şık bir hale gelir.
BU requirements gerekli mi? gerekliyse ingilizce yaz
2 adım tamamlandı
Evet, requirements.txt bu proje için gerekli ve faydalı; özellikle GitHub’a koyduğun için. Kısaca:

Projendeki tüm Python bağımlılıklarını ve versiyonlarını listeler.

Başka biri (veya sen, başka bir makinede) repoyu klonladığında tek komutla aynı ortamı kurabilir:
pip install -r requirements.txt

Ortamların aynı olmasını sağlar, “bende çalışıyor sende niye çalışmıyor” sorununu azaltır.

Bu yüzden README’de İngilizce şöyle bir bölüm yazmak mantıklı:

text
## Dependencies

All Python dependencies are listed in `requirements.txt`.

To install them:

```bash
pip install -r requirements.txt
```

This ensures you get the exact same library versions used in this project.
Bunu README’ye ekleyebilirsin; hocan veya başka biri repoyu açtığında ne yapacağını anlar.

pardonö readme'yi ingilizce yaz

Tabii — aşağıya projene uygun, temiz ve profesyonel bir İngilizce README bırakıyorum.

README.md
text
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
