from pydantic import BaseModel
from app.schema.mixins import EmailMixin, PasswordMixin, CodeMixin, TokenMixin


class RegisterIn(EmailMixin, PasswordMixin):
    pass


class RegisterOut(BaseModel):
    message: str = "Пользователь зарегистрирован"


class VerifyEmailIn(EmailMixin, CodeMixin):
    pass


class VerifyEmailOut(BaseModel):
    message: str = "Почта подтверждена"


class LoginIn(EmailMixin, PasswordMixin):
    pass


class LoginOut(TokenMixin):
    pass
