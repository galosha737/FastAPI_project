from datetime import datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, Field, StrictBool, field_validator

from .file import FileResponse


class PostBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Annotated[str, Field(min_length=3, max_length=255)]
    text: Annotated[str, Field(min_length=1, max_length=10000)]
    is_published: StrictBool = False
    location_id: Annotated[int | None, Field(default=None, gt=0)]
    category_id: Annotated[int | None, Field(default=None, gt=0)]

    @field_validator("title", "text", mode="before")
    @classmethod
    def required_strings_must_not_be_empty(cls, value):
        if isinstance(value, str):
            value = value.strip()
        if not value:
            raise ValueError("Field cannot be empty")
        return value


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Annotated[str | None, Field(default=None, min_length=3, max_length=255)]
    text: Annotated[str | None, Field(default=None, min_length=1, max_length=10000)]
    is_published: StrictBool | None = None
    location_id: Annotated[int | None, Field(default=None, gt=0)]
    category_id: Annotated[int | None, Field(default=None, gt=0)]

    @field_validator("title", "text", mode="before")
    @classmethod
    def optional_strings_empty_to_none(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                return None
        return value


class PostOut(BaseModel):
    id: int
    title: str
    text: str
    is_published: bool
    image: "FileResponse | None" = None
    author_id: int
    location_id: int | None = None
    category_id: int | None = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
