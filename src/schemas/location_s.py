from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StrictBool, field_validator


class LocationBase(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: Annotated[str, Field(min_length=1, max_length=255)]
    is_published: StrictBool = False

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if isinstance(value, str):
            value = value.strip()
        if not value:
            raise ValueError("Location name cannot be empty")
        return value


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    name: Annotated[str | None, Field(default=None, min_length=1, max_length=255)]
    is_published: StrictBool | None = None

    @field_validator("name", mode="before")
    @classmethod
    def empty_name_to_none(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                return None
        return value


class LocationOut(LocationBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)