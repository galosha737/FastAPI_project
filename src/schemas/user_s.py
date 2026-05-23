from datetime import datetime
from typing import Annotated
from pydantic import (BaseModel, ConfigDict, EmailStr, Field, SecretStr, field_validator)


class UserUpdate(BaseModel):
    first_name: Annotated[str | None, Field(default=None,
                          min_length=1, max_length=30)]
    last_name: Annotated[str | None, Field(default=None,
                         min_length=1, max_length=30)]
    bio_info: Annotated[str | None, Field(default=None, max_length=200)]
    email: EmailStr


class UserCreate(UserUpdate):
    username: Annotated[str, Field(min_length=5, max_length=30)]
    password: SecretStr

    @field_validator("username", "email", mode="before")
    @classmethod
    def strip_required_strings(cls, value: str) -> str:
        if isinstance(value, str):
            value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value


class UserOut(UserUpdate):
    id: int
    username: str
    active: bool
    date_joined: datetime
    model_config = ConfigDict(from_attributes=True)
