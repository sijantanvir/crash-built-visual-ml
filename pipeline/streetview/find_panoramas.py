import pandas as pd
from streetview import search_panoramas, get_panorama_meta


def find_panoramas(df: pd.DataFrame) -> pd.DataFrame:
    """
    For each point, retrieve available panoramas.
    """

    records = []

    for idx, row in df.iterrows():
        lat, lon = row["Lat"], row["Long"]

        try:
            panos = search_panoramas(lat, lon)
        except Exception:
            continue

        for pano in panos:
            date = pano.date

            # fallback if date missing
            if date is None:
                try:
                    meta = get_panorama_meta(pano_id=pano.pano_id)
                    date = meta.date
                except Exception:
                    continue

            records.append({
                "Lat": lat,
                "Long": lon,
                "pano_id": pano.pano_id,
                "date": date
            })

    return pd.DataFrame(records)