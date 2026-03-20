from sqlalchemy.orm import Session
from src.models.post_m import Post
from src.schems.post_s import PostCreate, PostUpdate
from typing import List, Optional


class PostRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_list(self, skip: int = 0, limit: int = 10) -> List[Post]:
        post_list = self.session.query(Post).offset(skip).limit(limit).all()
        return post_list  # type: ignore

    def get(self, post_id: int) -> Optional[Post]:
        return self.session.get(Post, post_id)

    def create(self, data: PostCreate) -> Post:
        post = Post(**data.model_dump())  # type: ignore
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return post

    def update(self, post_id: int, data: PostUpdate) -> Optional[Post]:
        post = self.get(post_id)
        if not post:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(post, field, value)
        self.session.commit()
        self.session.refresh(post)
        return post

    def delete(self, post_id: int) -> Optional[Post]:
        post = self.get(post_id)
        if not post:
            return None
        self.session.delete(post)
        self.session.commit()
        return post