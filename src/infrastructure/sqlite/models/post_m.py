from ..database import Base
from sqlalchemy import Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .mixin_m import PubAndCreate
from typing import Optional, List


class Post(Base, PubAndCreate):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    text: Mapped[str] = mapped_column(String(500))
    is_published: Mapped[bool] = mapped_column(Boolean, default=False)
    image: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, default=None)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    location_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("locations.id", ondelete="SET NULL"),
        nullable=True
    )
    location: Mapped[Optional["Location"]] = relationship("Location", back_populates="posts")
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True
    )
    category: Mapped[Optional["Category"]] = relationship("Category", back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan"
    )
