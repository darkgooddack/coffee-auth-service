from app.kafka.handlers.base import KafkaMessageHandler
from app.kafka.producer import get_kafka_producer
from app.schema.events import AuthRequest, AuthResponse
from app.database.db import new_session
from app.repository.user import UserRepository
from app.service.auth import AuthService
from app.core.logger import logger


class AuthRequestHandler(KafkaMessageHandler):
    topic = "user.auth.request"

    async def handle(self, payload: dict) -> None:
        response = AuthResponse(
            request_id=payload.get("request_id")
        )

        try:
            cmd = AuthRequest(**payload)

            async with new_session() as session:
                repo = UserRepository(session)
                auth_service = AuthService(repo)

                response.user_id, response.error = await auth_service.authenticate_token(cmd.token)

        except Exception:
            logger.exception("Auth handler failed")
            response.error = "internal_error"

        producer = await get_kafka_producer()
        await producer.send(
            "user.auth.response",
            response.model_dump()
        )
