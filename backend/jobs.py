from redis_client import redis_client, job_key

def get_job(job_id: str):
    key = job_key(job_id)
    data = redis_client.hgetall(key)

    if not data:
        return {
            "status": "not_found",
            "job_id": job_id
        }

    return data
