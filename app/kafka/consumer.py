import asyncio
import json
from aiokafka import AIOKafkaConsumer

from app.kafka.router import KafkaRouter
from app.core.config import settings
from app.core.logger import logger


class KafkaConsumerService:
    def __init__(self, router: KafkaRouter):
        self._router = router
        self._consumer: AIOKafkaConsumer | None = None
        self._task: asyncio.Task | None = None

    async def start(self):
        self._consumer = AIOKafkaConsumer(
            *self._router.topics,
            bootstrap_servers=[settings.kafka.servers],
            group_id="auth-service-dev",
            enable_auto_commit=False,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        await self._consumer.start()
        self._task = asyncio.create_task(self._consume())
        logger.info("Kafka consumer started")

    async def stop(self):
        if self._task:
            self._task.cancel()
        if self._consumer:
            await self._consumer.stop()

    async def _consume(self):
        try:
            async for message in self._consumer:
                await self._router.dispatch(
                    message.topic,
                    message.value,
                )
                await self._consumer.commit()
        except asyncio.CancelledError:
            pass
