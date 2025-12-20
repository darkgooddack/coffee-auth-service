from fastapi import HTTPException, status


class AppBaseError(Exception):
    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Сервисная ошибка"

    def http(self) -> HTTPException:
        return HTTPException(
            status_code=self.status_code,
            detail=self.detail
        )


class UserAlreadyExistsError(AppBaseError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Пользователь с такой почтой уже существует"


class InvalidCredentialsError(AppBaseError):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неверный логин или пароль"

class InvalidVerificationCodeError(AppBaseError):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Неверный код подтверждения"