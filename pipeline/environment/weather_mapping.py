import pandas as pd


WMO_MAP = {
    0: "Clear",
    1: "Mostly Clear",
    2: "Partly Cloudy",
    3: "Cloudy",
    45: "Fog",
    48: "Freezing Fog",
    51: "Light Drizzle",
    53: "Drizzle",
    55: "Heavy Drizzle",
    56: "Light Freezing Drizzle",
    57: "Freezing Drizzle",
    61: "Light Rain",
    63: "Rain",
    65: "Heavy Rain",
    66: "Light Freezing Rain",
    67: "Freezing Rain",
    71: "Light Snow",
    73: "Snow",
    75: "Heavy Snow",
    77: "Snow Grains",
    80: "Light Rain Shower",
    81: "Rain Shower",
    82: "Heavy Rain Shower",
    85: "Snow Shower",
    86: "Heavy Snow Shower",
    95: "Thunderstorm",
    96: "Hailstorm",
    99: "Heavy Hailstorm",
}


def map_weather_codes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert WMO weather codes to descriptions.
    """

    print("[Environment] Mapping weather codes...")

    df = df.copy()

    df["weather_description"] = df["weather_code"].map(WMO_MAP)

    return df