import redis
import json
import time
import os

from PIL import Image, ImageFilter

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)


worker_id = os.environ.get("HOSTNAME", "worker")


def log(message):

    print(message)

    redis_client.lpush("logs", message)

    redis_client.ltrim("logs", 0, 50)


log(f"{worker_id} iniciado")


while True:

    try:

        redis_client.hset(
            "workers_status",
            worker_id,
            json.dumps({
                "status": "active",
                "last_seen": str(time.strftime("%Y-%m-%d %H:%M:%S"))
            })
        )

        task_data = redis_client.lpop("tasks")

        if not task_data:

            time.sleep(1)

            continue

        task = json.loads(task_data)

        task_id = task["id"]

        filename = task["filename"]

        filepath = f"{UPLOAD_DIR}/{filename}"

        log(f"{worker_id} procesando {filename}")

        redis_client.hset(
            "tasks_status",
            task_id,
            json.dumps({
                "status": "processing"
            })
        )

        # SIMULAR PROCESAMIENTO LENTO
        time.sleep(5)

        image = Image.open(filepath)

        base_name = filename.rsplit(".", 1)[0]

        # =========================
        # CONVERTIR RGBA -> RGB
        # =========================

        if image.mode == "RGBA":
            image = image.convert("RGB")

        # =========================
        # RESIZE
        # =========================

        resized_name = f"{base_name}_resized.jpg"

        resized_path = f"{PROCESSED_DIR}/{resized_name}"

        resized = image.resize((800, 800))

        resized.save(resized_path)

        log(f"{worker_id} resize completado")

        # =========================
        # THUMBNAIL
        # =========================

        thumb_name = f"{base_name}_thumb.jpg"

        thumb_path = f"{PROCESSED_DIR}/{thumb_name}"

        thumb = image.copy()

        thumb.thumbnail((200, 200))

        thumb.save(thumb_path)

        log(f"{worker_id} thumbnail generado")

        # =========================
        # GRAYSCALE
        # =========================

        gray_name = f"{base_name}_gray.jpg"

        gray_path = f"{PROCESSED_DIR}/{gray_name}"

        gray = image.convert("L")

        gray.save(gray_path)

        log(f"{worker_id} grayscale completado")

        # =========================
        # PNG
        # =========================

        png_name = f"{base_name}.png"

        png_path = f"{PROCESSED_DIR}/{png_name}"

        image.save(png_path, "PNG")

        log(f"{worker_id} png generado")

        # =========================
        # BLUR
        # =========================

        blur_name = f"{base_name}_blur.jpg"

        blur_path = f"{PROCESSED_DIR}/{blur_name}"

        blur = image.filter(ImageFilter.BLUR)

        blur.save(blur_path)

        log(f"{worker_id} blur completado")

        # =========================
        # STATUS FINAL
        # =========================

        redis_client.hset(
            "tasks_status",
            task_id,
            json.dumps({
                "status": "completed",

                "resized": resized_name,

                "thumbnail": thumb_name,

                "grayscale": gray_name,

                "png": png_name,

                "blur": blur_name
            })
        )

        log(f"{worker_id} terminó {filename}")

    except Exception as e:

        log(f"ERROR {worker_id}: {str(e)}")

        time.sleep(2)
