from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List
from .user_s import UserOut
from .category_s import CategoryOut
from .location_s import LocationOut
from .comment_s import CommentOut


class PostUpdate(BaseModel):
    title: str = Field(default=None)
    text: str = Field(default=None)
    created_at: datetime = Field(default=None)
    is_published: bool = Field(default=None)
    image: str = Field(default=None)
    location_id: int = Field(default=None)
    category_id: int = Field(default=None)

class PostCreate(PostUpdate):
    author_id: int = Field(default=None)

class PostOut(PostCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PostDetail(PostOut):
    author: UserOut
    category: CategoryOut = Field(default=None)
    location: LocationOut = Field(default=None)
    comments: List["CommentOut"] = Field(default=[])
    model_config = ConfigDict(from_attributes=True)