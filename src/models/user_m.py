from src.infrastructure.sqlite.database import Base
from sqlalchemy import Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.post_m import Post
from src.models.comment_m import Comment
from typing import List
from datetime import datetime



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    bio_info: Mapped[str] = mapped_column(Text, default="")
    password: Mapped[str] = mapped_column(String, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    date_joined: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    posts: Mapped[List["Post"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )