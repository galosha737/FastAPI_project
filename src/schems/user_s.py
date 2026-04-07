from pydantic import BaseModel, Field, EmailStr, ConfigDict, SecretStr
from datetime import datetime
from typing import Annotated

class UserUpdate(BaseModel):
    first_name: Annotated[str | None, Field(default=None, min_length=1, max_length=30)]
    last_name: Annotated[str | None, Field(default=None, min_length=1, max_length=30)]
    bio_info: Annotated[str | None, Field(default=None, min_length=1, max_length=200)]
    email: Annotated[EmailStr | None, Field(default=None)]

class UserCreate(UserUpdate):
    username: Annotated[str, Field(min_length=5, max_length=30)]
    password: SecretStr

class UserOut(UserUpdate):
    id: int
    username: str
    active: bool
    date_joined: datetime
    model_config = ConfigDict(from_attributes=True)