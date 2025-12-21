from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.redis.broker_url,
    backend=settings.redis.backend_url
)

celery_app.conf.task_always_eager = False
celery_app.conf.task_create_missing_queues = True
celery_app.conf.worker_enable_remote_control = True

import app.tasks.email_tasks
import app.tasks.user_tasks
