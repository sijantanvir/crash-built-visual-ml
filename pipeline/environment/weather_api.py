import requests
import pandas as pd
from datetime import datetime


def _build_url(lat, lon, date):
    return (
        "https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={date}&end_date={date}"
        "&hourly=weather_code&timezone=auto"
    )


def _extract_hour(time_str):
    """
    Convert 12-hour time to 24-hour format.
    """
    return datetime.strptime(time_str, "%I:%M %p").strftime("%H")


def fetch_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Fetch weather codes for each crash record.
    """

    print("[Environment] Fetching weather data...")

    weather_codes = []

    for _, row in df.iterrows():
        lat = row["Lat"]
        lon = row["Long"]

        year = f"20{row['Year']}"
        month = str(row["Month"]).zfill(2)
        day = str(row["Date in month"]).zfill(2)

        date = f"{year}-{month}-{day}"
        hour = _extract_hour(row["Time(12h)"])

        try:
            url = _build_url(lat, lon, date)
            response = requests.get(url, timeout=10)
            data = response.json()

            found = None

            for t, code in zip(data["hourly"]["time"], data["hourly"]["weather_code"]):
                if t.endswith(f"{hour}:00"):
                    found = code
                    break

            weather_codes.append(found)

        except Exception:
            weather_codes.append(None)

    df = df.copy()
    df["weather_code"] = weather_codes

    return df