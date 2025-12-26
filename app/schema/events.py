from pydantic import BaseModel, EmailStr


class EmailVerificationSendCommand(BaseModel):
    email: EmailStr
    code: str


class UserRegisteredEvent(BaseModel):
    user_id: str


class AuthRequest(BaseModel):
    request_id: str
    token: str


class AuthResponse(BaseModel):
    request_id: str
    user_id: str | None = None
    error: str | None = None
