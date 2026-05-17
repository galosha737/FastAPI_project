from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class LocationUpdateAndCreate(BaseModel):
    name: Annotated[str, Field(min_length=1)]
    is_published: Annotated[bool, Field(default=False)]

class LocationOut(LocationUpdateAndCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)