import os
import uuid
from sqlalchemy import ForeignKey, Integer, String, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from ..database import Base


class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    original_filename: Mapped[str] = mapped_column(String, nullable=False)
    stored_filename: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger)
    mime_type: Mapped[str] = mapped_column(String)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), nullable=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey("comments.id"), nullable=True)
    post = relationship("Post", back_populates="image")
    comment = relationship("Comment", back_populates="image")

    @staticmethod
    def generate_stored_filename(original_filename: str) -> str:
        """Генерирует уникальное имя файла, сохраняя расширение."""
        name, ext = os.path.splitext(original_filename)
        unique_name = str(uuid.uuid4())
        return f"{unique_name}{ext}"