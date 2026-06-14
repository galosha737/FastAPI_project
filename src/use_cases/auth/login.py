from fastapi import HTTPException, status

from src.auth.security import create_access_token, verify_password
from src.exceptions.database import DatabaseError, DatabaseUnavailableError
from src.infrastructure.postgres.repositories.user_rep import UserRepository
from src.schemas.token import Token


class LoginUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, username: str, password: str) -> Token:
        try:
            user = await self.repository.get_by_username(username)

            if user is None or not verify_password(password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid username or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            access_token = create_access_token(data={"sub": str(user.id)})

            return Token(
                access_token=access_token,
                token_type="bearer",
            )

        except DatabaseUnavailableError as err:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database unavailable",
            ) from err

        except DatabaseError as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error",
            ) from err
