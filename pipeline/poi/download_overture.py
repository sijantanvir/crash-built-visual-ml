import duckdb
from pathlib import Path


def download_overture(output_path="data/raw/overture_places.parquet"):
    """
    Load Overture POI dataset via DuckDB (S3).
    """

    print("[POI] Loading Overture dataset...")

    con = duckdb.connect()

    query = """
    SELECT *
    FROM read_parquet(
        's3://overturemaps-us-west-2/release/2023-10-19-alpha.0/theme=places/*',
        filename=true
    )
    LIMIT 100000
    """

    df = con.execute(query).fetch_df()

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path)

    return output_path