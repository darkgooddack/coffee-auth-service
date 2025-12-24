import random
import uuid
import asyncio
from pydantic import EmailStr

from app.utils.celery_app import celery_app
from app.schema.events import EmailVerificationSendCommand, UserRegisteredEvent
from app.utils.redis_singleton import get_redis_cache
from app.utils.kafka_singleton import get_kafka_producer
from app.core.logger import logger


@celery_app.task(name="app.tasks.email.send_verification", bind=True)
def send_verification_email(self, email: EmailStr, user_id: uuid.UUID):
    async def task():
        logger.info(f"Starting email verification task for {email}")
        code = random.randint(10000, 99999)
        logger.info(f"Generated verification code: {code} for {email}")

        redis_cache = await get_redis_cache()
        kafka_producer = await get_kafka_producer()

        await redis_cache.set_verification_code(email, str(code))
        logger.info(f"Saved verification code in Redis for {email}")

        email_command = EmailVerificationSendCommand(email=email, code=str(code))
        user_registered_event = UserRegisteredEvent(user_id=str(user_id))

        await kafka_producer.send(topic="email.send.verification", payload=email_command.model_dump())
        logger.info(f"Sent EmailVerificationSendCommand to Kafka for {email}")

        await kafka_producer.send(topic="user.registered", payload=user_registered_event.model_dump())
        logger.info(f"Sent UserRegisteredEvent to Kafka for user_id={user_id}")

        await redis_cache.stop()
        await kafka_producer.stop()
        logger.info(f"Finished email verification task for {email}")

    asyncio.run(task())
