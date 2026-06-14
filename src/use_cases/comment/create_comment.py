from fastapi import HTTPException, status

from src.exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)
from src.infrastructure.postgres.models import Comment, User
from src.infrastructure.postgres.repositories.comment_rep import (
    CommentRepository,)
from src.schemas.comment_s import CommentCreate


class CreateCommentUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self,
                      data: CommentCreate,
                      current_user: User) -> Comment:
        text = data.text.strip()

        if not text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Comment text cannot be empty",
            )
        
        comment = Comment(
            text=data.text,
            author_id=current_user.id,
            post_id=data.post_id,
        )
        try:
            return await self.repository.create(comment)
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