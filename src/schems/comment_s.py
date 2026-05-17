from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class CommentUpdate(BaseModel):
    text: Annotated[str, Field(..., min_length=1, max_length=100)]

class CommentCreate(CommentUpdate):
    post_id: int
    author_id: int

class CommentOut(CommentCreate):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)