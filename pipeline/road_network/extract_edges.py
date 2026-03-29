import osmnx as ox


def extract_edges(df, buffer_dist=2000):
    """
    Extract nearest road edges for each crash point.
    """

    print("[Road] Extracting edges...")

    graphs = []

    for _, row in df.iterrows():
        lat, lon = row["Lat"], row["Long"]

        G = ox.graph_from_point(
            (lat, lon),
            dist=buffer_dist,
            network_type="drive"
        )

        graphs.append((row["id"], G, lat, lon))

    return graphs