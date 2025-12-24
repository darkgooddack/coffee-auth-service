from pydantic import BaseModel, EmailStr


class EmailVerificationSendCommand(BaseModel):
    email: EmailStr
    code: str

class UserRegisteredEvent(BaseModel):
    user_id: str
