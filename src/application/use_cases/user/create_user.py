from fastapi import HTTPException, status

from src.domain.exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)
from src.infrastructure.postgres.models import User
from src.infrastructure.postgres.repositories.user_rep import UserRepository
from src.presentation.schemas.user_s import UserCreate
from src.auth.security import get_hash_password


class CreateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, data: UserCreate) -> User:
        username = data.username.strip()
        password = data.password.get_secret_value().strip()
        email = str(data.email).strip()

        if not username or not password or not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="email, username and password cannot be empty",
            )

        hashed_password = get_hash_password(password)

        user = User(
            username=username,
            password=hashed_password,
            email=email,
            bio_info=data.bio_info,
            first_name=data.first_name,
            last_name=data.last_name,
            role="user",
        )

        try:
            return await self.repository.create(user)

        except DataConflictError as err:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(err),
            ) from err

        except ForeignKeyConflictError as err:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(err),
            ) from err

        except DatabaseUnavailableError as err:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(err),
            ) from err

        except DatabaseError as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err),
            ) from err