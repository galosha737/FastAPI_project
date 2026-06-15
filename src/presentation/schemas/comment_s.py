from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .file import FileResponse


class CommentBase(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    text: Annotated[str, Field(min_length=1, max_length=300)]

    @field_validator("text", mode="before")
    @classmethod
    def validate_text(cls, value):
        if isinstance(value, str):
            value = value.strip()
        if not value:
            raise ValueError("Comment text cannot be empty")
        return value


class CommentCreate(CommentBase):
    post_id: Annotated[int, Field(gt=0)]


class CommentUpdate(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )

    text: Annotated[str | None, Field(default=None, min_length=1, max_length=300)]

    @field_validator("text", mode="before")
    @classmethod
    def empty_text_to_none_or_error(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                return None
        return value


class CommentOut(CommentCreate):
    id: int
    created_at: datetime
    author_id: int
    image: FileResponse | None = None

    model_config = ConfigDict(from_attributes=True)