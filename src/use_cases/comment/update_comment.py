from fastapi import HTTPException, status

from exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)
from infrastructure.postgres.models import Comment, User
from infrastructure.postgres.repositories.comment_rep import (
    CommentRepository,)
from schemas.comment_s import CommentUpdate


class UpdateCommentUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self,
                      comment_id: int,
                      data: CommentUpdate,
                      current_user: User
                      ) -> Comment:
        comment = await self.repository.get(comment_id)
        if comment.author_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not the author of this comment",
            )
        if comment is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment with id={comment_id} not found",
            )
        try:
            update_data = data.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(comment, field, value)
            
            return await self.repository.update(comment)
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