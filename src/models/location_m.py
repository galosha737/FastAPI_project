from src.infrastructure.sqlite.database import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.mixin_m import PubAndCreate
from src.models.post_m import Post
from typing import List


class Location(Base, PubAndCreate):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    posts: Mapped[List["Post"]] = relationship(back_populates="location")