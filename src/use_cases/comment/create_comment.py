from fastapi import HTTPException, status, UploadFile

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
from src.use_cases.file_use_case import FileUseCase


class CreateCommentUseCase:
    def __init__(self, repository: CommentRepository,  file_use_case: FileUseCase):
        self.repository = repository
        self.file_use_case = file_use_case

    async def execute(self,
                      data: CommentCreate,
                      image: UploadFile | None,
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
            created_comment = await self.repository.create(comment)
            if image and image.filename:
                await self.file_use_case.handle_file_upload(image, created_comment.id, "comment")

            refreshed_comment = await self.repository.get(created_comment.id) 
            if refreshed_comment is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Comment not found immediately after creation, this is an internal error.",
                )
            return refreshed_comment
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