from fastapi import HTTPException, status

from src.exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
)
from src.infrastructure.postgres.models.user_m import User
from src.infrastructure.postgres.repositories.user_rep import UserRepository
from src.schemas.user_s import ChangeUserRoleRequest
from src.config import settings


class ChangeUserRoleUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: int, data: ChangeUserRoleRequest, requesting_user: User) -> User:
        new_role = data.role
        allowed_roles = settings.ALLOWED_ROLES
        if new_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role."
            )
        
        user = await self.repository.get(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id={user_id} not found",
            )
        
        if user.id == requesting_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Super Admin cannot change his role."
            )
        
        user.role = new_role

        try:
            updated_user = await self.repository.update(user)
            return updated_user
        except DataConflictError as err:
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
