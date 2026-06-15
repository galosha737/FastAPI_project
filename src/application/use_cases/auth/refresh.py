from fastapi import HTTPException, status
import logging

from src.auth.security import decode_token, create_access_token
from src.domain.exceptions.database import DatabaseError, DatabaseUnavailableError
from src.infrastructure.postgres.repositories.user_rep import UserRepository
from src.presentation.schemas.token import Token

logger = logging.getLogger(__name__)


class RefreshTokenUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, refresh_token: str) -> Token:
        logger.info("Executing RefreshTokenUseCase with provided refresh_token")
        try:
            logger.debug(f"Attempting to decode refresh token: {refresh_token[:10]}...")
            payload = decode_token(refresh_token)
            logger.debug(f"Decoded payload: {payload}")
            if payload is None:
                logger.warning("Failed to decode refresh token or token is invalid/expired.")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
            user_id_str = payload.get("sub")
            logger.debug(f"Extracted user_id from token payload: {user_id_str}")
            if user_id_str is None:
                logger.warning("No 'sub' claim found in refresh token payload.")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid refresh token"
                )
            try:
                user_id = int(user_id_str)
            except ValueError as err:
                logger.warning(f"Invalid token subject format, expected integer, got: {user_id_str}")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token subject format"
                ) from err
            logger.info(f"Fetching user from database with ID: {user_id}")
            user = await self.repository.get(user_id)
            logger.debug(f"Fetched user from DB: {user is not None}")
            if user is None:
                logger.warning(f"User with ID {user_id} not found in database.")
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found"
                )
            
            logger.info(f"User {user_id} found. Generating new access token.")
            new_access_token = create_access_token(data={"sub": str(user.id)})
            logger.info("New access token generated successfully.")

            logger.info("Returning new token pair.")
            return Token(
                access_token=new_access_token,
                refresh_token=refresh_token,
                token_type="bearer",
            )

        except DatabaseUnavailableError as err:
            logger.error(f"Database unavailable error during refresh: {err}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database unavailable",
            ) from err

        except DatabaseError as err:
            logger.error(f"General database error during refresh: {err}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Database error",
            ) from err
