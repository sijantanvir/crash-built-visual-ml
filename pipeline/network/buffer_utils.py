import pyproj
from shapely.geometry import Point
from shapely.ops import transform
from functools import partial


def create_buffer(lat, lon, radius=500):
    """
    Create circular buffer (in meters) around a point.
    """

    center = Point(lon, lat)

    project_to_m = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:4326'),
        pyproj.Proj(init='epsg:3857')
    )

    project_to_deg = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:3857'),
        pyproj.Proj(init='epsg:4326')
    )

    center_m = transform(project_to_m, center)
    buffer_m = center_m.buffer(radius)
    buffer_deg = transform(project_to_deg, buffer_m)

    return buffer_deg