from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class LocationUpdateAndCreate(BaseModel):
    name: str = Field(default=None)
    is_published: bool = Field(default=None)

class LocationOut(LocationUpdateAndCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)