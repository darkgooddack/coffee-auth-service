from app.core.logger import logger
from app.core.security import hash_password, verify_password, create_token_pair
from app.models.user import User
from app.schema.auth import RegisterOut, RegisterIn, LoginIn, LoginOut, VerifyEmailIn, VerifyEmailOut
from app.utils.error import UserAlreadyExistsError, InvalidCredentialsError, InvalidVerificationCodeError
from app.tasks.email_tasks import send_verification_email
from app.tasks.user_tasks import confirm_email_task
from app.utils.redis_singleton import get_redis_cache


class UserService:
    def __init__(self, repo):
        self.repo = repo


    async def register(self, data: RegisterIn) -> RegisterOut:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise UserAlreadyExistsError()

        user = User(
            email=data.email,
            hash_password=hash_password(data.password)
        )

        user = await self.repo.save_user(user)

        send_verification_email.delay(data.email, user.id)

        return RegisterOut(message="Пользователь зарегистрирован")


    @staticmethod
    async def verify(data: VerifyEmailIn) -> VerifyEmailOut:

        redis_cache = await get_redis_cache()

        stored_code = await redis_cache.get_verification_code(data.email)
        if stored_code is None or str(stored_code) != str(data.code):
            raise InvalidVerificationCodeError("Неверный код подтверждения")
        logger.info(f"Before confirm_email_task {data.email}")
        confirm_email_task.delay(data.email)

        return VerifyEmailOut(message="Почта подтверждена")


    async def login(self, data: LoginIn) -> LoginOut:
        user = await self.repo.get_by_email(data.email)
        if not user or not verify_password(data.password, str(user.hash_password)):
            raise InvalidCredentialsError()
        return create_token_pair(str(user.id))
