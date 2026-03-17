from src.infrastructure.sqlite.database import Base
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.mixin_m import PubAndCreate
from src.models.user_m import User
from typing import Optional


class Post(Base, PubAndCreate):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    location_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("locations.id", ondelete="SET NULL"),
        nullable=True
    )
    location: Mapped[Optional["Location"]] = relationship(back_populates="posts")
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True
    )
    category: Mapped[Optional["Category"]] = relationship(back_populates="posts")