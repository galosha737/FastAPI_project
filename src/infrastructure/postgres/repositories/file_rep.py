from sqlalchemy.ext.asyncio import AsyncSession
from src.infrastructure.postgres.models.file import File


class FileRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_file(self, file_instance: File) -> File:
        """Создаёт запись файла в БД."""
        self.session.add(file_instance)
        await self.session.flush()
        await self.session.refresh(file_instance)
        return file_instance
