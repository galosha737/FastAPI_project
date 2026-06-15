from fastapi import HTTPException, status, UploadFile

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
from src.use_cases.file_use_case import FileUseCase


class CreatePostUseCase:
    def __init__(self, repository: PostRepository, file_use_case: FileUseCase):
        self.repository = repository
        self.file_use_case = file_use_case 

    async def execute(self,
                      data: PostCreate,
                      image: UploadFile | None,
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
            category_id=data.category_id,
            location_id=data.location_id,
            author_id=current_user.id,
        )
        try:
            created_post = await self.repository.create(post)
            if image and image.filename:
                await self.file_use_case.handle_file_upload(image, created_post.id, "post")

            refreshed_post = await self.repository.get(created_post.id)
            if refreshed_post is None:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Post not found immediately after creation, this is an internal error.",
                )
            return refreshed_post
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
