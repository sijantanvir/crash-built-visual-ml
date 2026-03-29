import pandas as pd
from pathlib import Path


def _safe_merge(left, right, on_cols, how="left"):
    """
    Safe merge with basic validation.
    """
    if right is None or len(right) == 0:
        return left

    return left.merge(right, on=on_cols, how=how)


def merge_all_features(
    road_df: pd.DataFrame,
    streetview_df: pd.DataFrame,
    poi_df: pd.DataFrame,
    network_df: pd.DataFrame,
    env_df: pd.DataFrame,
    config: dict
) -> pd.DataFrame:
    """
    Merge all feature sources into a single dataset.
    """

    print("[Merge] Starting feature merge...")

    df = road_df.copy()

    # --- merge streetview ---
    if streetview_df is not None:
        df = _safe_merge(
            df,
            streetview_df,
            on_cols=["id", "Lat", "Long"]
        )

    # --- merge POI ---
    if poi_df is not None:
        df = _safe_merge(
            df,
            poi_df,
            on_cols=["id"]
        )

    # --- merge network ---
    if network_df is not None:
        df = _safe_merge(
            df,
            network_df,
            on_cols=["id"]
        )

    # --- merge environment ---
    if env_df is not None:
        df = _safe_merge(
            df,
            env_df,
            on_cols=["id"]
        )

    # --- basic cleaning ---
    df = df.drop_duplicates()

    # optional: drop rows with missing target
    if "severity" in df.columns:
        df = df.dropna(subset=["severity"])

    # --- save ---
    output_path = Path(config["paths"]["processed_data"])
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"[Merge] Final dataset saved → {output_path}")
    print(f"[Merge] Shape: {df.shape}")

    return df