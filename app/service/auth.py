from jose import JWTError

from app.repository.user import UserRepository
from app.core.security import decode_access_token


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo

    async def authenticate_token(self, token: str) -> tuple[str | None, str | None]:
        try:
            payload = decode_access_token(token)
            user_id = payload.get("sub")
            if not user_id:
                return None, "invalid_token"

            user = await self._user_repo.get_by_id(user_id)
            if not user:
                return None, "user_not_found"

            return str(user.id), None

        except JWTError:
            return None, "invalid_token"
        except Exception:
            return None, "internal_error"
