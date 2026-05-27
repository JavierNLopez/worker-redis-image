from redis import Redis
from rq import Worker, Queue

redis_conn = Redis(
    host="redis",
    port=6379
)

queue = Queue(
    connection=redis_conn
)

worker = Worker(
    [queue],
    connection=redis_conn
)

print("Worker iniciado")

worker.work()
