from fastapi import FastAPI
from src.infrastructure.sqlite.database import Base, engine

# Создание таблиц бд
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello FastAPI with Poetry!"}
