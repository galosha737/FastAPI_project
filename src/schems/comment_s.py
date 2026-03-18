from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class CommentUpdate(BaseModel):
    text: str = Field(default=None)

class CommentCreate(CommentUpdate):
    post_id: int
    author_id: int

class CommentOut(CommentCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)