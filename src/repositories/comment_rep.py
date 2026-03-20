from sqlalchemy.orm import Session
from src.models.comment_m import Comment
from src.schems.comment_s import CommentCreate, CommentUpdate
from typing import List, Optional

class CommentRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_list(self, skip: int = 0, limit: int = 10) -> List[Comment]:
        comment_list = self.session.query(Comment).offset(skip).limit(limit).all()
        return comment_list # type: ignore

    def get(self, comment_id: int) -> Optional[Comment]:
        return self.session.get(Comment, comment_id)

    def create(self, data: CommentCreate) -> Comment:
        comment = Comment(**data.model_dump()) # type: ignore
        self.session.add(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def update(self, comment_id: int, data: CommentUpdate) -> Optional[Comment]:
        comment = self.get(comment_id)
        if not comment:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(comment, field, value)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    def delete(self, comment_id: int) -> Optional[Comment]:
        comment = self.get(comment_id)
        if not comment:
            return None
        self.session.delete(comment)
        self.session.commit()
        return comment