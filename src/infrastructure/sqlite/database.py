from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

# Строка подключения
SQLALCHEMY_DATABASE_URL = settings.database_url
# Создание движка (в аргументе разрешаем многопоточность)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
# Создание класса-построителя для создания объекта сессии базы данных при помощи функции-фабрики
SessionLocal = sessionmaker(autoflush=False, bind=engine)
# Создание базовой модели для таблиц бд
Base = declarative_base()
# Определяем зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()