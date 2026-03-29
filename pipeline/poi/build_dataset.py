from .download_overture import download_overture
from .filter_bbox import filter_bbox
from .spatial_processing import extract_centroid
from .buffer_features import compute_poi_density
from .tfidf_features import compute_tfidf_features


def build_poi_dataset(config, crash_df):

    parquet_path = download_overture()

    bbox = config.get("poi_bbox")
    poi_df = filter_bbox(parquet_path, bbox)

    poi_df = extract_centroid(poi_df)

    # TF-IDF features
    tfidf_df = compute_tfidf_features(poi_df, crash_df)

    return tfidf_df

def build_poi_dataset(config, crash_df):
    """
    Full POI pipeline.
    """

    print("[POI] Building POI feature dataset...")

    # Step 1: Download
    parquet_path = download_overture()

    # Step 2: Filter region (Dhaka example)
    bbox = config.get("poi_bbox", (90.3, 90.5, 23.6, 23.9))
    poi_df = filter_bbox(parquet_path, bbox)

    # Step 3: Convert to lat/lon
    poi_df = extract_centroid(poi_df)

    # Step 4: Compute features
    poi_features = compute_poi_density(
        poi_df,
        crash_df,
        radius=config["params"]["buffer_radius"]
    )

    print("[POI] Completed")

    return poi_features