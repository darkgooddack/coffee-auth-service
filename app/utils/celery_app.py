from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "worker",
    broker=settings.redis.broker_url,
    backend=settings.redis.backend_url
)

import app.tasks.email_tasks
import app.tasks.user_tasks
