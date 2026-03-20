from src.infrastructure.sqlite.database import Base
from sqlalchemy import Integer, String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.mixin_m import PubAndCreate
from typing import List



class Category(Base, PubAndCreate):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    posts: Mapped[List["Post"]] = relationship("Post", back_populates="category")
    is_published: Mapped[bool] = mapped_column(Boolean)