from infrastructure.postgres.models import Category
from infrastructure.postgres.repositories.category_rep import (
    CategoryRepository,)
from schemas.category_s import CategoryCreate


class CreateCategoryUseCase:
    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def execute(self, data: CategoryCreate) -> Category:
        category = Category(
            title=data.title,
            slug=data.slug,
            description=data.description,
            is_published=data.is_published,
        )
        return await self.repository.create(category)