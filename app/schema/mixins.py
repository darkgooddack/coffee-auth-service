import re
import uuid

from pydantic import BaseModel, EmailStr, Field, field_validator


class EmailMixin(BaseModel):
    email: EmailStr


class UserIdMixin(BaseModel):
    id: uuid.UUID


class PasswordMixin(BaseModel):
    password: str = Field(min_length=8, max_length=128)

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")
        if not re.search(r"\d", value):
            raise ValueError("Пароль должен содержать хотя бы одну цифру")
        return value


class CodeMixin(BaseModel):
    code: str = Field(min_length=5, max_length=5)

    @field_validator("code")
    def validate_code(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("Код должен состоять только из цифр")
        return value


class TokenMixin(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
