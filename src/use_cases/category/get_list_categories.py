from infrastructure.postgres.models import Category
from infrastructure.postgres.repositories.category_rep import (
    CategoryRepository,)


class GetCategoryListUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self,
                      *,
                      skip: int = 0,
                      limit: int = 10) -> list[Category]:
        return await self.repository.get_list(skip=skip, limit=limit)
