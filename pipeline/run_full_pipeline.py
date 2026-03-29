import yaml
import pandas as pd

# Road
from pipeline.road_network.extract_edges import extract_edges
from pipeline.road_network.segment_roads import segment_roads
from pipeline.road_network.compute_bearing import compute_bearing

# StreetView
from pipeline.streetview.generate_points import generate_points
from pipeline.streetview.find_panoramas import find_panoramas
from pipeline.streetview.select_closest_year import select_closest_year
from pipeline.streetview.download_images import download_images

# POI
from pipeline.poi.build_dataset import build_poi_dataset

# Network
from pipeline.network.compute_network_density import compute_network_density

# Environment
from pipeline.environment.weather_api import fetch_weather_data
from pipeline.environment.weather_mapping import map_weather_codes

# Merge
from pipeline.merge.merge_all_features import merge_all_features

# Model
from models.train_xgboost import train_model


def load_config(path="config.yaml"):
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main():
    config = load_config()

    print("===================================")
    print(" Starting Full Pipeline Execution ")
    print("===================================")

    # ----------------------------------
    # 1. Load raw crash data
    # ----------------------------------
    crash_df = pd.read_csv(config["paths"]["raw_data"])
    crash_df["id"] = crash_df.index

    # ----------------------------------
    # 2. Road Network
    # ----------------------------------
    graphs = extract_edges(crash_df)
    points = segment_roads(graphs)
    road_df = compute_bearing(points)

    # ----------------------------------
    # 3. Street View
    # ----------------------------------
    sv_points = generate_points(points)
    pano_df = find_panoramas(sv_points)
    streetview_df = select_closest_year(pano_df, crash_df)

    # Optional (disable for speed)
    if config.get("download_images", False):
        download_images(streetview_df, config)

    # ----------------------------------
    # 4. POI Features
    # ----------------------------------
    poi_df = build_poi_dataset(config, crash_df)

    # ----------------------------------
    # 5. Network Density
    # ----------------------------------
    network_df = compute_network_density(crash_df)

    # ----------------------------------
    # 6. Environment (Weather)
    # ----------------------------------
    env_df = fetch_weather_data(crash_df)
    env_df = map_weather_codes(env_df)

    # ----------------------------------
    # 7. Merge
    # ----------------------------------
    final_df = merge_all_features(
        road_df=road_df,
        streetview_df=streetview_df,
        poi_df=poi_df,
        network_df=network_df,
        env_df=env_df,
        config=config
    )

    # ----------------------------------
    # 8. Model Training
    # ----------------------------------
    train_model(final_df, config)

    print("===================================")
    print(" Pipeline Completed Successfully ")
    print("===================================")


if __name__ == "__main__":
    main()