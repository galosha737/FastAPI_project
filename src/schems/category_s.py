from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CategoryUpdateAndCreate(BaseModel):
    slug: str = Field(default=None)
    title: str = Field(default=None)
    description: str = Field(default=None)
    is_published: bool = Field(default=None)

class CategoryOut(CategoryUpdateAndCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)