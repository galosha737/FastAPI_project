from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base
from .mixin_m import PubAndCreate


class Category(Base, PubAndCreate):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="category")
    is_published: Mapped[bool] = mapped_column(Boolean, 
                                               nullable=False, 
                                               default=False)
