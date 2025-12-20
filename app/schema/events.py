from pydantic import BaseModel, EmailStr, Field


class EmailVerificationEvent(BaseModel):
    email: EmailStr
    code: int = Field(ge=10000, le=99999)
