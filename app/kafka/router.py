from app.kafka.handlers.base import KafkaMessageHandler
from app.core.logger import logger


class KafkaRouter:
    def __init__(self, handlers: list[KafkaMessageHandler]):
        self._handlers = {h.topic: h for h in handlers}

    @property
    def topics(self) -> list[str]:
        return list(self._handlers.keys())

    async def dispatch(self, topic: str, payload: dict):
        handler = self._handlers.get(topic)

        if not handler:
            logger.warning(f"No handler for topic {topic}")
            return

        await handler.handle(payload)
