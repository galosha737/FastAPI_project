import re
from datetime import datetime
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    field_validator,
    model_validator,
)

SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def normalize_slug(value: str) -> str:
    value = re.sub(r"[\s_]+", "-", value.lower())
    value = re.sub(r"[^a-z0-9-]", "", value)
    value = re.sub(r"-{2,}", "-", value)
    value = value.strip("-")

    if not value:
        raise ValueError("slug cannot be empty")

    if not SLUG.match(value):
        raise ValueError("invalid slug format")

    return value


class CategoryBase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Annotated[str, Field(min_length=3, max_length=255)]
    description: Annotated[str | None, Field(default=None, max_length=1000)]
    is_published: StrictBool = False

    @field_validator("description", mode="before")
    @classmethod
    def empty_description_to_none(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                return None
        return value


class CategoryCreate(CategoryBase):
    slug: Annotated[str | None, Field(default=None, min_length=3, max_length=100)]

    @model_validator(mode="after")
    def set_slug_from_title(self):
        if self.slug is None:
            self.slug = self.title
        self.slug = normalize_slug(self.slug)
        return self


class CategoryUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    title: Annotated[str | None, Field(default=None, min_length=3, max_length=255)]
    slug: Annotated[str | None, Field(default=None, min_length=3, max_length=100)]
    description: Annotated[str | None, Field(default=None, max_length=1000)]
    is_published: StrictBool | None = None

    @field_validator("slug")
    @classmethod
    def normalize_slug_validator(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return normalize_slug(value)

    @field_validator("description", mode="before")
    @classmethod
    def empty_description_to_none(cls, value):
        if isinstance(value, str):
            value = value.strip()
            if value == "":
                return None
        return value


class CategoryOut(CategoryBase):
    id: int
    slug: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)