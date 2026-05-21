from fastapi import HTTPException, status

from exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)
from infrastructure.postgres.models import User
from infrastructure.postgres.repositories.user_rep import (
    UserRepository,)
from schemas.user_s import UserUpdate


class UpdateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self,
                      user_id: int,
                      data: UserUpdate
                      ) -> User:
        user = await self.repository.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={user_id} not found",
            )
        try:
            update_data = data.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(user, field, value)
            
            return await self.repository.update(user)
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
