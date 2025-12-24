from pydantic import EmailStr
import asyncio

from app.utils.celery_app import celery_app
from app.utils.redis_singleton import get_redis_cache
from app.repository.user import UserRepository
from app.database.db import new_session
from app.core.logger import logger


@celery_app.task(name="app.tasks.user.confirm_email", bind=True)
def confirm_email_task(self, email: EmailStr):
    async def task():
        redis_cache = await get_redis_cache()
        logger.info(f"Deleting verification code for {email}")
        await redis_cache.delete_verification_code(email)
        logger.info(f"Verification code deleted for {email}")

        async with new_session() as session:
            repo = UserRepository(session)
            user = await repo.get_by_email(email)
            if user:
                user.confirmed = True
                await repo.save_user(user)
                logger.info(f"User {email} marked as confirmed in DB")

        await redis_cache.stop()
        logger.info(f"Redis connection closed for {email}")

    asyncio.run(task())
