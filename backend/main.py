from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

import redis
import uuid
import json
import os
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

app.mount("/processed", StaticFiles(directory=PROCESSED_DIR), name="processed")


@app.get("/")
def home():
    return {"message": "Backend funcionando"}


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    task_id = str(uuid.uuid4())

    filename = f"{task_id}_{file.filename}"

    filepath = f"{UPLOAD_DIR}/{filename}"

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    task = {
        "id": task_id,
        "filename": filename
    }

    redis_client.rpush("tasks", json.dumps(task))

    redis_client.hset(
        "tasks_status",
        task_id,
        json.dumps({
            "status": "queued"
        })
    )

    return {
        "task_id": task_id
    }


@app.get("/status/{task_id}")
def get_status(task_id: str):

    data = redis_client.hget("tasks_status", task_id)

    if not data:
        return {
            "status": "not_found"
        }

    return json.loads(data)


@app.get("/dashboard")
def dashboard():

    workers = redis_client.hgetall("workers_status")

    workers_data = {}

    for key, value in workers.items():

        try:
            workers_data[key] = json.loads(value)
        except:
            pass

    queued = 0
    processing = 0
    completed = 0

    tasks = redis_client.hgetall("tasks_status")

    for _, value in tasks.items():

        try:
            task = json.loads(value)

            status = task.get("status")

            if status == "queued":
                queued += 1

            elif status == "processing":
                processing += 1

            elif status == "completed":
                completed += 1

        except:
            pass

    logs = redis_client.lrange("logs", 0, 20)

    return {
        "workers": len(workers_data),
        "queued": queued,
        "processing": processing,
        "completed": completed,
        "workers_status": workers_data,
        "logs": logs
    }
