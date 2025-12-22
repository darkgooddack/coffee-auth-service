import random
import asyncio
import uuid

from pydantic import EmailStr

from app.utils.celery_app import celery_app
from app.schema.events import EmailVerificationSendCommand, UserRegisteredEvent
from app.utils.redis_singleton import get_redis_cache
from app.utils.kafka_singleton import get_kafka_producer
from asgiref.sync import async_to_sync


@celery_app.task(name="app.tasks.email.send_verification", bind=True)
def send_verification_email(self, email: EmailStr, user_id: uuid.UUID):
    async def task():
        # code = random.randint(10000, 99999)
        code = 12345

        redis_cache = await get_redis_cache()
        kafka_producer = await get_kafka_producer()

        await redis_cache.set_verification_code(email, str(code))

        email_command = EmailVerificationSendCommand(email=email, code=str(code))
        user_registered_event = UserRegisteredEvent(user_id=user_id)

        await kafka_producer.send(topic="email.send.verification", payload=email_command.model_dump())
        await kafka_producer.send(topic="user.registered", payload=user_registered_event.model_dump())

        await redis_cache.stop()
        await kafka_producer.stop()

    async_to_sync(task)()
