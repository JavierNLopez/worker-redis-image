from PIL import Image, ImageFilter
from redis import Redis

import os
import json
import time

redis_conn = Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

PROCESSED_DIR = "processed"

os.makedirs(PROCESSED_DIR, exist_ok=True)

def update_status(
    task_id,
    status,
    image_url=None,
    message=None
):

    data = {
        "status": status
    }

    if image_url:
        data["image_url"] = image_url

    if message:
        data["message"] = message

    redis_conn.set(
        f"task:{task_id}",
        json.dumps(data)
    )

def process_image(
    filepath,
    task_id
):

    try:

        update_status(
            task_id,
            "processing"
        )

        print(f"Procesando {task_id}")

        time.sleep(2)

        img = Image.open(filepath)

        # Resize
        img = img.resize((800, 800))

        time.sleep(2)

        # Blur filter
        img = img.filter(
            ImageFilter.BLUR
        )

        time.sleep(2)

        # Thumbnail
        img.thumbnail((300, 300))

        output_name = f"{task_id}.png"

        output_path = os.path.join(
            PROCESSED_DIR,
            output_name
        )

        img.save(
            output_path,
            "PNG"
        )

        image_url = (
            f"/processed/{output_name}"
        )

        update_status(
            task_id,
            "completed",
            image_url=image_url
        )

        print(f"Completado {task_id}")

    except Exception as e:

        update_status(
            task_id,
            "error",
            message=str(e)
        )

        print(str(e))
