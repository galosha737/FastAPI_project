from pydantic import BaseModel, Field, EmailStr, ConfigDict
from datetime import datetime

class UserUpdate(BaseModel):
    first_name: str = Field()
    last_name: str = Field()
    bio_info: str = Field()
    email: EmailStr = Field()

class UserCreate(UserUpdate):
    nickname: str
    password: str

class UserOut(UserUpdate):
    id: int
    nickname: str
    active: bool
    date_joined: datetime
    model_config = ConfigDict(from_attributes=True)