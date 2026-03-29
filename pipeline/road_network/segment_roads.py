import networkx as nx
import osmnx as ox
from shapely.geometry import LineString
from shapely.ops import transform

from .utils import get_projections


def _get_linestring(G, u, v):
    edge_data = G[u][v][0]

    if "geometry" in edge_data:
        return edge_data["geometry"], edge_data["length"]

    # fallback: reconstruct path
    route = nx.shortest_path(G, u, v)
    nodes, _ = ox.graph_to_gdfs(G)

    coords = nodes.loc[route]["geometry"].tolist()
    line = LineString(coords)

    return line, edge_data["length"]


def _get_interval(length):
    if length < 20:
        return 5
    elif length > 2000:
        return 50
    else:
        return 10


def segment_roads(graphs):
    """
    Convert edges into evenly spaced points.
    """

    print("[Road] Segmenting roads...")

    project_to_meters, project_to_degrees = get_projections()

    all_points = []

    for idx, G, lat, lon in graphs:

        u, v = ox.nearest_edges(G, lon, lat)

        line, length = _get_linestring(G, u, v)

        line_m = transform(project_to_meters, line)

        interval = _get_interval(length)

        num_steps = int(line_m.length / interval)

        for i in range(num_steps + 1):
            point = line_m.interpolate(i * interval)
            point_deg = transform(project_to_degrees, point)

            all_points.append({
                "id": idx,
                "Lat": point_deg.y,
                "Long": point_deg.x
            })

    return all_points