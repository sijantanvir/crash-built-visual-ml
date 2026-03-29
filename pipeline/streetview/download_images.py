import os
import time
import requests
from streetview import get_streetview


def download_images(df, config):
    """
    Download images for selected panoramas.
    """

    save_dir = config["paths"]["images_dir"]
    os.makedirs(save_dir, exist_ok=True)

    api_key = config["api_keys"]["google"]

    for idx, row in df.iterrows():
        pano_id = row["pano_id"]
        heading = row.get("Bearing", 0)

        # Metadata check
        url = f"https://maps.googleapis.com/maps/api/streetview/metadata?pano={pano_id}&key={api_key}"

        try:
            meta = requests.get(url).json()
        except Exception:
            continue

        if meta.get("status") != "OK":
            continue

        try:
            img = get_streetview(
                pano_id=pano_id,
                api_key=api_key,
                width=640,
                height=640,
                fov=60,
                pitch=0,
                heading=heading
            )

            filename = os.path.join(save_dir, f"{idx}.jpg")
            img.save(filename)

            time.sleep(1.5)

        except Exception:
            continue
