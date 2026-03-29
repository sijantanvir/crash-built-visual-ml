import pandas as pd
from datetime import datetime


def select_closest_year(pano_df: pd.DataFrame, crash_df: pd.DataFrame) -> pd.DataFrame:
    """
    Match each point with closest panorama date.
    """

    results = []

    for idx, row in crash_df.iterrows():
        lat, lon = row["Lat"], row["Long"]
        crash_date = datetime.strptime(row["Date"], "%Y-%m")

        subset = pano_df[
            (pano_df["Lat"] == lat) & (pano_df["Long"] == lon)
        ]

        if subset.empty:
            continue

        # parse dates
        subset = subset.copy()
        subset["parsed_date"] = pd.to_datetime(subset["date"], errors="coerce")

        subset = subset.dropna(subset=["parsed_date"])

        if subset.empty:
            continue

        closest_idx = (subset["parsed_date"] - crash_date).abs().idxmin()

        selected = subset.loc[closest_idx]

        results.append({
            "Lat": lat,
            "Long": lon,
            "pano_id": selected["pano_id"],
            "pano_date": selected["date"],
            "crash_date": row["Date"]
        })

    return pd.DataFrame(results)