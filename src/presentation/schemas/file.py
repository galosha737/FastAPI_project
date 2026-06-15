from pydantic import BaseModel, computed_field
from datetime import datetime

from src.core.config import STATIC_IMAGES_URL


class FileBase(BaseModel):
    original_filename: str
    file_path: str
    file_size: int
    mime_type: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class FileResponse(FileBase):
    id: int
    stored_filename: str

    @computed_field
    @property
    def url(self) -> str:
        return f"{STATIC_IMAGES_URL}/{self.stored_filename}"
