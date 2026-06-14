from fastapi import HTTPException, status

from src.exceptions.database import (
    DatabaseError,
    DatabaseUnavailableError,
)
from src.infrastructure.postgres.models import Post
from src.infrastructure.postgres.repositories.post_rep import (
    PostRepository,)


class GetPostListUseCase:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def execute(self,
                      *,
                      skip: int = 0,
                      limit: int = 10) -> list[Post]:
        try:
            if skip < 0 | limit <= 0 | limit >= 100:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Incorrect arguments",
                )
            return await self.repository.get_list(skip=skip, limit=limit)
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