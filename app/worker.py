from celery import Celery
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

celery = Celery(
    "tasks",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks"]
)

celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    worker_pool="solo"  # <-- Add this line
)
