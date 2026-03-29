import osmnx as ox
import pandas as pd


def compute_bearing(points):
    """
    Compute bearing between consecutive points.
    """

    print("[Road] Computing bearings...")

    df = pd.DataFrame(points)

    bearings = []

    for i in range(len(df)):
        if i == len(df) - 1:
            bearings.append(bearings[-1])
            continue

        lat1, lon1 = df.loc[i, ["Lat", "Long"]]
        lat2, lon2 = df.loc[i + 1, ["Lat", "Long"]]

        b = ox.bearing.calculate_bearing(lat1, lon1, lat2, lon2)
        bearings.append(b)

    df["Bearing"] = bearings

    return df