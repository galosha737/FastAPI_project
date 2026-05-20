from infrastructure.postgres.models import Category
from infrastructure.postgres.repositories.category_rep import (
    CategoryRepository,)
from exceptions.category import CategoryNotFound


class GetCategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, category_id: int) -> Category:
        category = await self.repository.get(category_id)
        if category is None:
            raise CategoryNotFound(category_id)
        return category
