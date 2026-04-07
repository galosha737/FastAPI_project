from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, model_validator


class CategoryUpdateAndCreate(BaseModel):
    title: Annotated[str, Field(min_length=3, max_length=255)]
    slug: Annotated[str | None, Field(default=None, min_length=3, max_length=100)]
    description: Annotated[str | None, Field(default=None, max_length=1000)]
    is_published: Annotated[bool, Field(default=False)]

    @model_validator(mode="after")
    def set_slug_from_title(self) -> "CategoryUpdateAndCreate":
        if self.slug is None:
            self.slug = self.title.lower()
        return self


class CategoryOut(CategoryUpdateAndCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)