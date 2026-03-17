from datetime import datetime
from src.infrastructure.sqlite.database import Base
from sqlalchemy import Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.post_m import Post
from src.models.user_m import User

class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")
