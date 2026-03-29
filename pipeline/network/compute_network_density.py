import math
import pandas as pd
import osmpy

from .buffer_utils import create_buffer


def _compute_road_length(polygon):
    """
    Compute total road length inside polygon using osmpy.
    """

    res = osmpy.get("RoadLength", polygon)

    total_length = 0.0

    for val in res.length:
        try:
            total_length += float(val)
        except Exception:
            continue

    return total_length


def compute_network_density(df: pd.DataFrame, radius=500) -> pd.DataFrame:
    """
    Compute road network density for each location.
    """

    print("[Network] Computing network density...")

    densities = []

    for _, row in df.iterrows():
        lat, lon = row["Lat"], row["Long"]

        try:
            buffer_polygon = create_buffer(lat, lon, radius)
            total_length = _compute_road_length(buffer_polygon)

            # density = length / area
            area = math.pi * (radius ** 2)
            density = total_length / area

        except Exception:
            density = None

        densities.append(density)

    df = df.copy()
    df["network_density"] = densities

    return df