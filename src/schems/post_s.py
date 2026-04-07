from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Annotated
from .user_s import UserOut
from .category_s import CategoryOut
from .location_s import LocationOut
from .comment_s import CommentOut


class PostUpdate(BaseModel):
    title: Annotated[str | None, Field(default=None)]
    text: Annotated[str | None, Field(default=None)]
    is_published: Annotated[bool, Field(default=False)]
    image: Annotated[str | None, Field(default=None)]
    location_id: Annotated[int | None, Field(default=None)]
    category_id: Annotated[int | None, Field(default=None)]

class PostCreate(PostUpdate):
    author_id: Annotated[int, Field(...)]

class PostOut(PostCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class PostDetail(PostOut):
    author: Annotated[UserOut, Field(...)]
    category: Annotated[CategoryOut | None, Field(default=None)]
    location: Annotated[LocationOut | None, Field(default=None)]
    comments: Annotated[List[CommentOut], Field(default_factory=list)]
