from src.infrastructure.sqlite.database import Base
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.mixin_m import PubAndCreate
from src.models.post_m import Post
from typing import List



class Category(Base, PubAndCreate):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    posts: Mapped[List["Post"]] = relationship(back_populates="category")