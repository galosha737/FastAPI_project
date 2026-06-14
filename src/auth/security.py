from datetime import UTC, datetime, timedelta
from typing import Any

from jose import jwt, JWTError
from pwdlib import PasswordHash

from src.config import settings

# Объект для работы с хешированием пароля
password_hash = PasswordHash.recommended()


def get_hash_password(password: str) -> str:
    '''Превращает пароль в хеш'''
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''Проверка совпадения пароля и хеша'''
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    '''Создает токен c данными и сроком действия'''
    to_encode = data.copy()

    expire = datetime.now(UTC) + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    # Добавляем время истечение в поле JWT "expiration time"
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_AUTH_KEY.get_secret_value(), algorithm=settings.AUTH_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    '''Расшифровывает токен и достает из него данные'''
    try:
        return jwt.decode(token, settings.SECRET_AUTH_KEY.get_secret_value(), algorithms=[settings.AUTH_ALGORITHM])
    except JWTError as err:
        raise ValueError("Invalid or expired token") from err