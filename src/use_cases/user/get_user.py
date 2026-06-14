from fastapi import HTTPException, status

from src.exceptions.database import (
    DatabaseError,
    DatabaseUnavailableError,
)
from src.infrastructure.postgres.models import User
from src.infrastructure.postgres.repositories.user_rep import (
    UserRepository,)


class GetUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> User:
        try:
            if user_id <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="user_id must be greater than 0",
                )
            user = await self.repository.get(user_id)
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with id={user_id} not found",
                )
            return user
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
