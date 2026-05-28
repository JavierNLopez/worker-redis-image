from PIL import Image, ImageFilter
import os
import time
import json
import redis

redis_conn = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

UPLOAD_FOLDER = "uploads"

RESIZED_FOLDER = "processed/resized"
FILTERED_FOLDER = "processed/filtered"
CONVERTED_FOLDER = "processed/converted"
THUMB_FOLDER = "processed/thumbnails"

os.makedirs(RESIZED_FOLDER, exist_ok=True)
os.makedirs(FILTERED_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)
os.makedirs(THUMB_FOLDER, exist_ok=True)


def update_status(task_id, status, extra=None):

    data = {
        "task_id": task_id,
        "status": status
    }

    if extra:
        data.update(extra)

    redis_conn.set(
        f"task:{task_id}",
        json.dumps(data)
    )

    redis_conn.publish(
        "tasks",
        json.dumps(data)
    )


def process_image(task_id, filename):

    try:

        worker_name = os.getenv("HOSTNAME", "worker")

        update_status(
            task_id,
            "processing",
            {
                "worker": worker_name
            }
        )

        input_path = f"{UPLOAD_FOLDER}/{filename}"

        image = Image.open(input_path)

        # ======================
        # 1. REDIMENSIONAR
        # ======================

        resized = image.resize((600, 600))

        resized_name = f"{task_id}_resized.png"

        resized_path = f"{RESIZED_FOLDER}/{resized_name}"

        resized.save(resized_path)

        # ======================
        # 2. FILTRO
        # ======================

        filtered = resized.filter(ImageFilter.DETAIL)

        filtered_name = f"{task_id}_filtered.png"

        filtered_path = f"{FILTERED_FOLDER}/{filtered_name}"

        filtered.save(filtered_path)

        # ======================
        # 3. CONVERTIR FORMATO
        # ======================

        converted_name = f"{task_id}.jpg"

        converted_path = f"{CONVERTED_FOLDER}/{converted_name}"

        filtered.convert("RGB").save(
            converted_path,
            "JPEG"
        )

        # ======================
        # 4. MINIATURA
        # ======================

        thumb = filtered.copy()

        thumb.thumbnail((150, 150))

        thumb_name = f"{task_id}_thumb.jpg"

        thumb_path = f"{THUMB_FOLDER}/{thumb_name}"

        thumb.save(thumb_path)

        time.sleep(2)

        update_status(
            task_id,
            "completed",
            {
                "worker": worker_name,

                "resized":
                f"/processed/resized/{resized_name}",

                "filtered":
                f"/processed/filtered/{filtered_name}",

                "converted":
                f"/processed/converted/{converted_name}",

                "thumbnail":
                f"/processed/thumbnails/{thumb_name}"
            }
        )

        return "ok"

    except Exception as e:

        update_status(
            task_id,
            "error",
            {
                "error": str(e)
            }
        )

        return str(e)
