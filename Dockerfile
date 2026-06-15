FROM python:3.13-slim

# Делаем немного чище образ: убираем лишний мусор и
# убираем буферизацию вывода
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock* /app/
# Отключаем у Poetry создание отдельного окружения,
# пусть пакеты ставятся прямо в окружение контейнера
RUN poetry config virtualenvs.create false && poetry install --no-root

COPY ./src /app/src
COPY ./alembic /app/alembic
COPY ./alembic.ini /app/

EXPOSE 8000