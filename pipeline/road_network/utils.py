import pandas as pd


def generate_points(segments):
    """
    Convert road segments into dataframe format.
    """

    df = pd.DataFrame(segments, columns=["Lat", "Long", "Bearing"])
    return df