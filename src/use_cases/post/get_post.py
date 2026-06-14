from fastapi import HTTPException, status

from src.exceptions.database import (
    DatabaseError,
    DatabaseUnavailableError,
)
from src.infrastructure.postgres.models import Post
from src.infrastructure.postgres.repositories.post_rep import (
    PostRepository,)


class GetPostUseCase:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def execute(self, post_id: int) -> Post:
        try:
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
            return post
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

