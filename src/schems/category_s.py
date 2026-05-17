import re
from datetime import datetime
from typing import Annotated

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


class CategoryUpdateAndCreate(BaseModel):
    title: Annotated[str, Field(min_length=3, max_length=255)]
    slug: Annotated[str | None, Field(default=None,
                                      min_length=3,
                                      max_length=100)]
    description: Annotated[str | None, Field(default=None, max_length=1000)]
    is_published: Annotated[bool, Field(default=False)]

    @model_validator(mode="after")
    def set_slug_from_title(self) -> CategoryUpdateAndCreate:
        if self.slug is None:
            self.slug = self.title.lower()
        return self

    @field_validator('slug', mode='after')
    @classmethod
    def normalize_slug_validator(cls, slug: str) -> str:
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = re.sub(r'[^a-z0-9-]', '', slug)
        slug = re.sub(r'-{2,}', '-', slug)
        slug = slug.strip('-')
        if not SLUG.match(slug):
            raise ValueError('invalid slug format')
        return slug


class CategoryOut(CategoryUpdateAndCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
