import os
import time
import json
import signal
import sys

import boto3
import redis
from botocore.exceptions import BotoCoreError, ClientError


# =========================
# ENV VARIABLES
# =========================

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET")


if not SQS_QUEUE_URL:
    print("ERROR: SQS_QUEUE_URL no definida", flush=True)
    sys.exit(1)

if not S3_BUCKET:
    print("WARNING: S3_BUCKET no definida (uploads desactivados)", flush=True)


# =========================
# CLIENTS
# =========================

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

sqs = boto3.client("sqs", region_name=AWS_REGION)
s3 = boto3.client("s3", region_name=AWS_REGION)


# =========================
# REDIS CHECK
# =========================

while True:
    try:
        if r.ping():
            print("Redis is connected", flush=True)
            break
    except Exception as e:
        print(f"Waiting Redis... {e}", flush=True)
        time.sleep(3)

print("Redis is active", flush=True)


# =========================
# SHUTDOWN HANDLER
# =========================

run = True

def handle_signal(signum, frame):
    global run
    print(f"Signal {signum} received, stopping worker...", flush=True)
    run = False

signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)


# =========================
# PROCESS LOGIC
# =========================

def process_message(body: dict):
    job_id = body.get("id")
    filename = body.get("filename")

    print(f"Processing job {job_id} -> {filename}", flush=True)

    # Mark in Redis
    r.set(f"job:{job_id}", "processing")

    # Simulate work
    time.sleep(2)

    # Optional S3 upload simulation
    if S3_BUCKET:
        try:
            s3.put_object(
                Bucket=S3_BUCKET,
                Key=f"processed/{filename}",
                Body=b"processed-data"
            )
            print(f"Uploaded {filename} to S3", flush=True)
        except (BotoCoreError, ClientError) as e:
            print(f"S3 error: {e}", flush=True)

    r.set(f"job:{job_id}", "done")
    print(f"Job {job_id} completed", flush=True)


# =========================
# MAIN LOOP (SQS)
# =========================

print("Worker started, waiting for SQS messages...", flush=True)

while run:
    try:
        response = sqs.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )

        messages = response.get("Messages", [])

        if not messages:
            continue

        for msg in messages:
            body = json.loads(msg["Body"])

            process_message(body)

            sqs.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"]
            )

    except (BotoCoreError, ClientError) as e:
        print(f"AWS error: {e}", flush=True)
        time.sleep(5)

    except Exception as e:
        print(f"Unexpected error: {e}", flush=True)
        time.sleep(3)


print("Worker stopped.", flush=True)
