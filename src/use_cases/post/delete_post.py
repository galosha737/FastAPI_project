from fastapi import HTTPException, status

from exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)
from infrastructure.postgres.repositories.post_rep import (
    PostRepository,)


class DeletePostUseCase:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def execute(self, post_id: int) -> None:

        if post_id <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="post_id must be greater than 0",
            )
        post = await self.repository.get(post_id)
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id={post_id} not found",
            )
        try:
            await self.repository.delete(post)
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