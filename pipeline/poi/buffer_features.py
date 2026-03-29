import pandas as pd
import numpy as np


def _haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # meters

    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)

    dphi = np.radians(lat2 - lat1)
    dlambda = np.radians(lon2 - lon1)

    a = np.sin(dphi/2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(dlambda/2)**2
    return 2 * R * np.arcsin(np.sqrt(a))


def compute_poi_density(poi_df, crash_df, radius=500):
    """
    Compute POI density around crash points.
    """

    print("[POI] Computing buffer features...")

    features = []

    for _, crash in crash_df.iterrows():
        lat_c, lon_c = crash["Lat"], crash["Long"]

        distances = _haversine(
            lat_c,
            lon_c,
            poi_df["Lat"].values,
            poi_df["Long"].values
        )

        nearby = poi_df[distances <= radius]

        features.append({
            "id": crash["id"],
            "poi_count": len(nearby)
        })

    return pd.DataFrame(features)