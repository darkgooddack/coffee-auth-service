from asgiref.sync import async_to_sync
from pydantic import EmailStr

from app.utils.celery_app import celery_app
from app.utils.redis_singleton import get_redis_cache
from app.repository.user import UserRepository
from app.database.db import new_session
from app.models.user import User
import asyncio


@celery_app.task(name="app.tasks.user.confirm_email", bind=True)
def confirm_email_task(self, email: EmailStr):
    async def task():
        redis_cache = await get_redis_cache()
        await redis_cache.delete_verification_code(email)

        async with new_session() as session:
            repo = UserRepository(session)
            user = await repo.get_by_email(email)
            if user:
                user.confirmed = True
                await repo.save_user(user)

        await redis_cache.stop()

    async_to_sync(task)()
