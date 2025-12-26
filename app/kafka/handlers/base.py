from abc import ABC, abstractmethod


class KafkaMessageHandler(ABC):
    topic: str

    @abstractmethod
    async def handle(self, payload: dict) -> None:
        ...
