import os

import aiofiles
from fastapi import HTTPException, UploadFile, status

from src.config import IMAGES_DIR, PROJECT_ROOT
from src.infrastructure.postgres.models.file import File
from src.infrastructure.postgres.repositories.file_rep import FileRepository

IMAGES_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/gif",
}


class FileUseCase:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    async def save_upload_file(
        self,
        file: UploadFile,
        content: bytes,
    ) -> tuple[str, str]:
        """Сохраняет файл в images и возвращает относительный путь и имя."""
        stored_filename = File.generate_stored_filename(file.filename)
        file_location = IMAGES_DIR / stored_filename

        async with aiofiles.open(file_location, "wb") as buffer:
            await buffer.write(content)

        relative_file_path = os.path.relpath(file_location, start=PROJECT_ROOT)
        return relative_file_path, stored_filename

    async def handle_file_upload(
        self,
        file: UploadFile,
        entity_id: int,
        entity_type: str,
    ) -> File:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Filename is required",
            )

        if file.content_type not in ALLOWED_IMAGE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"File type {file.content_type} not allowed. "
                    f"Allowed types: {sorted(ALLOWED_IMAGE_TYPES)}"
                ),
            )

        content = await file.read()
        if not content:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uploaded file is empty",
            )

        relative_file_path, stored_filename = await self.save_upload_file(
            file,
            content,
        )

        file_data = {
            "original_filename": file.filename,
            "stored_filename": stored_filename,
            "file_path": relative_file_path.replace("\\", "/"),
            "file_size": len(content),
            "mime_type": file.content_type,
        }

        if entity_type == "post":
            file_data["post_id"] = entity_id
        elif entity_type == "comment":
            file_data["comment_id"] = entity_id
        else:
            raise ValueError(f"Unsupported entity type: {entity_type}")

        db_file = File(**file_data)
        return await self.file_repository.create_file(db_file)
