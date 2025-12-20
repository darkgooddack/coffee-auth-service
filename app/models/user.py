import datetime
import uuid

from pydantic import EmailStr
from sqlalchemy import String, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )
    email: Mapped[EmailStr] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )
    hash_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    confirmed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        server_default=func.now()
    )
    