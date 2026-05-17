from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .mixin_m import PubAndCreate
from ..database import Base


class Location(Base, PubAndCreate):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    is_published: Mapped[bool] = mapped_column(Boolean)
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="location")