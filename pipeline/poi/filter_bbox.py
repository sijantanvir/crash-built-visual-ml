import duckdb


def filter_bbox(parquet_path, bbox):
    """
    Filter POIs within bounding box.
    bbox = (xmin, xmax, ymin, ymax)
    """

    print("[POI] Filtering by bounding box...")

    xmin, xmax, ymin, ymax = bbox

    con = duckdb.connect()

    query = f"""
    SELECT *
    FROM read_parquet('{parquet_path}')
    WHERE bbox.xmin > {xmin}
      AND bbox.xmax < {xmax}
      AND bbox.ymin > {ymin}
      AND bbox.ymax < {ymax}
    """

    df = con.execute(query).fetch_df()

    return df