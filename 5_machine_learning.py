import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def run_ml_model():
    print("--- Starting Machine Learning Model (Linear Regression) ---")

    # Forecast verisi kullan — 320 satır, anlamlı model için yeterli
    try:
        df = pd.read_csv("data/processed/forecast_weather_clean.csv")
        print(f"SUCCESS: Forecast data loaded ({len(df)} rows).")
    except FileNotFoundError:
        print("ERROR: Run 2b_forecast_transform.py first.")
        return

    if len(df) < 20:
        print("Not enough data to train the model.")
        return

    # Features: humidity + wind → Target: temperature
    X = df[["humidity_percent", "wind_speed_m_s"]]
    y = df["temperature_c"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    print("SUCCESS: Model trained.")

    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    r2  = r2_score(y_test, predictions)

    print(f"MSE : {mse:.2f}")
    print(f"R²  : {r2:.4f}")
    print(f"Coefficients — humidity: {model.coef_[0]:.4f} | wind: {model.coef_[1]:.4f}")
    print(f"Intercept    : {model.intercept_:.4f}")
    print("--- Machine Learning Phase Completed ---")

if __name__ == "__main__":
    run_ml_model()