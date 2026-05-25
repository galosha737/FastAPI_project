from fastapi import HTTPException, status

from exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)
from infrastructure.postgres.models import Post, User
from infrastructure.postgres.repositories.post_rep import (
    PostRepository,)
from schemas.post_s import PostUpdate


class UpdatePostUseCase:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def execute(self,
                      post_id: int,
                      data: PostUpdate,
                      current_user: User,
                      ) -> Post:
        post = await self.repository.get(post_id)
        if post.author_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the author of this post",
            )
        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id={post_id} not found",
            )
        try:
            update_data = data.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(post, field, value)
            
            return await self.repository.update(post)
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
