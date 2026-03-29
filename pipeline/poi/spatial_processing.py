import pandas as pd


def extract_centroid(df: pd.DataFrame):
    """
    Convert bbox → centroid lat/lon.
    """

    print("[POI] Extracting centroids...")

    df = df.copy()

    df["Lat"] = (df["bbox.ymin"] + df["bbox.ymax"]) / 2
    df["Long"] = (df["bbox.xmin"] + df["bbox.xmax"]) / 2

    return df