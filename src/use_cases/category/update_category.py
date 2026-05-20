from infrastructure.postgres.models import Category
from infrastructure.postgres.repositories.category_rep import (
    CategoryRepository,)
from schemas.category_s import CategoryUpdate
from exceptions.category import CategoryNotFound


class UpdateCategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self,
                      category_id: int,
                      data: CategoryUpdate
                      ) -> Category:
        category = await self.repository.get(category_id)
        if category is None:
            raise CategoryNotFound
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(category, field, value)
        
        return await self.repository.update(category)
