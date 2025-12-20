import random
from app.utils.celery_app import celery_app
from app.schema.events import EmailVerificationEvent
from app.utils.redis_singleton import get_redis_cache
from app.utils.kafka_singleton import get_kafka_producer

@celery_app.task(name="app.tasks.email.send_verification", bind=True)
async def send_verification_email(self, email: str):
    #code = random.randint(10000, 99999)
    code = 12345

    redis_cache = await get_redis_cache()
    kafka_producer = await get_kafka_producer()

    await redis_cache.set_verification_code(email, code)

    event = EmailVerificationEvent(email=email, code=code)
    await kafka_producer.send("verify.notification.email", event.model_dump())
