import json
from aiokafka import AIOKafkaProducer
from app.core.config import settings

class KafkaProducerWrapper:
    def __init__(self):
        self._producer: AIOKafkaProducer | None = None

    async def start(self):
        if self._producer is None:
            self._producer = AIOKafkaProducer(
                bootstrap_servers=[settings.kafka.servers],
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            )
            await self._producer.start()

    async def stop(self):
        if self._producer:
            await self._producer.stop()
            self._producer = None

    async def send(self, topic: str, payload: dict):
        if self._producer is None:
            await self.start()
        await self._producer.send_and_wait(topic, payload)


kafka_producer_singleton: KafkaProducerWrapper | None = None

async def get_kafka_producer() -> KafkaProducerWrapper:
    global kafka_producer_singleton
    if kafka_producer_singleton is None:
        kafka_producer_singleton = KafkaProducerWrapper()
        await kafka_producer_singleton.start()
    return kafka_producer_singleton
