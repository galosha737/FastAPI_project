from infrastructure.postgres.repositories.category_rep import (
    CategoryRepository,)
from exceptions.category import CategoryNotFound


class DeleteCategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, category_id: int) -> None:
        category = await self.repository.get(category_id)
        if category is None:
            raise CategoryNotFound(category_id)
        
        await self.repository.delete(category)