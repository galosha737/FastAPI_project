from fastapi import HTTPException, status

from src.domain.exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)
from src.infrastructure.postgres.models import Category
from src.infrastructure.postgres.repositories.category_rep import (
    CategoryRepository,)
from src.presentation.schemas.category_s import CategoryCreate


class CreateCategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, data: CategoryCreate) -> Category:
        title = data.title.strip()
        slug = data.slug

        if not title or not slug:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Title and slug cannot be empty",
            )

        category = Category(
            title=data.title,
            slug=data.slug,
            description=data.description,
            is_published=data.is_published,
        )
        try:
            return await self.repository.create(category)
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
