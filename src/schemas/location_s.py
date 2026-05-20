from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class LocationBase(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=255)]
    is_published: bool = False


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: Annotated[str | None, Field(min_length=1, max_length=255)] = None
    is_published: bool | None = None


class LocationOut(LocationBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)