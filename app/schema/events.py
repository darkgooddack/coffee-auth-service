from pydantic import BaseModel, EmailStr


class EmailVerificationEvent(BaseModel):
    email: EmailStr
    code: str
