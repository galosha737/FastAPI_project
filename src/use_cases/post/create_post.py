from fastapi import HTTPException, status

from src.exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)
from src.infrastructure.postgres.models import Post, User
from src.infrastructure.postgres.repositories.post_rep import (
    PostRepository,)
from src.schemas.post_s import PostCreate


class CreatePostUseCase:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def execute(self,
                      data: PostCreate,
                      current_user: User) -> Post:
        if current_user.id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="authentication required",
            )
        post = Post(
            title=data.title,
            is_published=data.is_published,
            text=data.text,
            image=data.image,
            category_id=data.category_id,
            location_id=data.location_id,
            author_id=current_user.id,
        )
        try:
            return await self.repository.create(post)
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
