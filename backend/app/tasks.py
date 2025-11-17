from celery import Celery
from .core.config import settings

broker = settings.CELERY_BROKER
backend = settings.CELERY_BACKEND

worker = Celery('resume_agent', broker=broker, backend=backend)

@worker.task
def long_running_task(x):
    # placeholder for processing (e.g., transcode, long AI jobs)
    return x * 2
