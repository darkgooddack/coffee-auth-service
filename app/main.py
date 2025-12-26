from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.core.config import settings
from app.core.logger import logger
from app.utils.error import AppBaseError
from app.api.auth import router as auth_router

from app.kafka.consumer import KafkaConsumerService
from app.kafka.router import KafkaRouter
from app.kafka.handlers.auth import AuthRequestHandler


kafka_router = KafkaRouter(
    handlers=[
        AuthRequestHandler(),
    ]
)

kafka_consumer = KafkaConsumerService(kafka_router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Kafka consumer...")
    await kafka_consumer.start()
    try:
        yield
    finally:
        logger.info("Stopping Kafka consumer...")
        await kafka_consumer.stop()


app = FastAPI(
    name="coffee-auth-service",
    description="Сервис аутентификации",
    lifespan=lifespan,
)


@app.exception_handler(AppBaseError)
async def app_base_error_handler(
    request: Request,
    exc: AppBaseError,
):
    raise exc.http()


app.include_router(auth_router, prefix=settings.api.prefix)


@app.get("/health")
async def health():
    return {"status": "ok"}
