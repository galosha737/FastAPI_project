from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.category_m import Category


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[Category]:
        s = select(Category).offset(skip).limit(limit)
        result = await self.session.execute(s)
        return list(result.scalars().all())

    async def get(self, category_id: int) -> Category | None:
        return await self.session.get(Category, category_id)

    async def create(self, category: Category) -> Category:
        self.session.add(category)
        await self.session.flush()
        await self.session.refresh(category)
        return category

    async def update(self, category: Category) -> Category:
        await self.session.flush()
        await self.session.refresh(category)
        return category

    async def delete(self, category: Category) -> None:
        await self.session.delete(category)
        await self.session.flush()
        return None
