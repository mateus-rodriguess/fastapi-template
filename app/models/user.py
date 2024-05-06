import re
import uuid as uuid_pkg
from datetime import datetime
from typing import Optional

from pydantic import EmailStr, validator
from sqlmodel import AutoString, Field, SQLModel


def validate_password(value: str) -> str:
    if len(value) < 8:
        raise ValueError("Password must be at least 6 characters long.")
    if not re.search(r"\W", value):
        raise ValueError(
            "Password must contain at least one special character."
        )
    if not re.search(r"[A-Z]", value):
        raise ValueError(
            "Password must contain at least one uppercase letter."
        )
    return value


class UserBase(SQLModel):
    uuid: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    email: EmailStr = Field(unique=True, index=True, sa_type=AutoString)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


class UserCreate(UserBase):
    password: str
    _validate_password = validator("password", allow_reuse=True)(
        validate_password
    )


class UserUpdate(UserBase):
    email: EmailStr | None = None
    password: str | None = None
    full_name: str | None = None
    _validate_password = validator("password", allow_reuse=True)(
        validate_password
    )


class UserRegister(SQLModel):
    email: EmailStr
    password: str
    full_name: str | None = None
    _validate_password = validator("password", allow_reuse=True)(
        validate_password
    )


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str

    _validate_password = validator("new_password", allow_reuse=True)(
        validate_password
    )


class UserPublic(UserBase):
    uuid: uuid_pkg.UUID
    created_at: datetime
    updated_at: datetime


class TokenPayload(SQLModel):
    sub: uuid_pkg.UUID | None = None


class TokenResponse(SQLModel):
    access_token: str
    refresh: str = None
    token_type: str = "Bearer"


class Message(SQLModel):
    detail: str = "Any message"


class User(UserBase, table=True):
    password: str
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    updated_at: Optional[datetime] = Field(
        default_factory=datetime.now,
        sa_column_kwargs={"onupdate": datetime.now},
        nullable=False,
    )


class UserAllowedFilters(SQLModel):
    uuid: Optional[uuid_pkg.UUID] = None
    sort_by: Optional[str] = "created_at"
    full_name: Optional[str] = None
