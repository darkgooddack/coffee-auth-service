import redis.asyncio as aioredis
import json
from typing import Any

from pydantic import EmailStr

from app.core.config import settings

class RedisCache:
    def __init__(self, url: str = settings.redis.url):
        self._url = url
        self.client: aioredis.Redis | None = None

    async def start(self):
        if self.client is None:
            self.client = aioredis.from_url(self._url, decode_responses=True)

    async def stop(self):
        if self.client:
            await self.client.close()
            self.client = None

    async def get(self, key: str) -> Any | None:
        if self.client is None:
            await self.start()
        data = await self.client.get(key)
        if data is None:
            return None
        try:
            return json.loads(data)
        except json.JSONDecodeError:
            return data

    async def set(self, key: str, value: Any, expire: int = 300):
        if self.client is None:
            await self.start()
        await self.client.set(key, json.dumps(value), ex=expire)

    async def set_verification_code(self, email: EmailStr, code: str, ttl: int = 300):
        await self.set(f"email_verification:{email}", code, expire=ttl)

    async def get_verification_code(self, email: str) -> int | None:
        code = await self.get(f"email_verification:{email}")
        if code is None:
            return None
        return int(code)

    async def delete_verification_code(self, email: EmailStr):
        if self.client is None:
            await self.start()
        await self.client.delete(f"email_verification:{email}")


redis_cache_singleton: RedisCache | None = None

async def get_redis_cache() -> RedisCache:
    global redis_cache_singleton
    if redis_cache_singleton is None:
        redis_cache_singleton = RedisCache()
        await redis_cache_singleton.start()
    return redis_cache_singleton
