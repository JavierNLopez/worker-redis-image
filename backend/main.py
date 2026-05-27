from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sse_starlette.sse import EventSourceResponse

from redis import Redis
from rq import Queue

from uuid import uuid4

import os
import json
import asyncio

from tasks import process_image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

redis_conn = Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

queue = Queue(connection=redis_conn)

UPLOAD_DIR = "uploads"
PROCESSED_DIR = "processed"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

app.mount(
    "/processed",
    StaticFiles(directory=PROCESSED_DIR),
    name="processed"
)

@app.get("/")
async def root():
    return {
        "message": "Backend funcionando"
    }

@app.post("/upload")
async def upload_image(
    file: UploadFile = File(...)
):

    task_id = str(uuid4())

    filename = f"{task_id}_{file.filename}"

    filepath = os.path.join(
        UPLOAD_DIR,
        filename
    )

    with open(filepath, "wb") as f:
        f.write(await file.read())

    redis_conn.set(
        f"task:{task_id}",
        json.dumps({
            "status": "pending"
        })
    )

    queue.enqueue(
        process_image,
        filepath,
        task_id
    )

    return {
        "task_id": task_id,
        "status": "pending"
    }

@app.get("/status/{task_id}")
async def status(task_id: str):

    data = redis_conn.get(
        f"task:{task_id}"
    )

    if not data:

        return JSONResponse(
            status_code=404,
            content={
                "error": "Task not found"
            }
        )

    return json.loads(data)

@app.get("/events/{task_id}")
async def events(task_id: str):

    async def event_generator():

        last_status = None

        while True:

            data = redis_conn.get(
                f"task:{task_id}"
            )

            if data:

                parsed = json.loads(data)

                if parsed["status"] != last_status:

                    last_status = parsed["status"]

                    yield {
                        "event": "message",
                        "data": json.dumps(parsed)
                    }

                    if parsed["status"] in [
                        "completed",
                        "error"
                    ]:
                        break

            await asyncio.sleep(1)

    return EventSourceResponse(
        event_generator()
    )
