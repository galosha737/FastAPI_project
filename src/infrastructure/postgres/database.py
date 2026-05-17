from typing import AsyncIterator
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings

# Строка подключения
SQLALCHEMY_DATABASE_URL = settings.postgres_url
# Создание движка
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Проверка соединения перед использованием
)
# Создание класса-построителя для создания объекта
# сессии базы данных при помощи функции-фабрики
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


# Создание базовой модели для таблиц бд
class Base(DeclarativeBase):
    pass


# Определяем зависимость
async def get_db() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
