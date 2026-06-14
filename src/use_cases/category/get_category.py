from fastapi import HTTPException, status

from src.exceptions.database import (
    DatabaseError,
    DatabaseUnavailableError,
)
from src.infrastructure.postgres.models import Category
from src.infrastructure.postgres.repositories.category_rep import (
    CategoryRepository,)


class GetCategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, category_id: int) -> Category:
        try:
            if category_id <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="category_id must be greater than 0",
                )
            category = await self.repository.get(category_id)
            if category is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Category with id={category_id} not found",
                )
            return category
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
