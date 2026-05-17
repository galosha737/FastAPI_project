from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.category_m import Category
from ....schems.category_s import CategoryUpdateAndCreate


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[Category]:
        s = select(Category).offset(skip).limit(limit)
        result = await self.session.execute(s)
        return list(result.scalars().all())

    async def get(self, category_id: int) -> Category | None:
        return await self.session.get(Category, category_id)

    async def create(self, data: CategoryUpdateAndCreate) -> Category:
        category = Category(**data.model_dump())
        self.session.add(category)
        await self.session.flush()
        await self.session.refresh(category)
        return category

    async def update(self,
                     category_id: int,
                     data: CategoryUpdateAndCreate) -> Category | None:
        category = await self.get(category_id)
        if not category:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(category, field, value)

        await self.session.flush()
        await self.session.refresh(category)
        return category

    async def delete(self, category_id: int) -> Category | None:
        category = await self.get(category_id)
        if not category:
            return None

        await self.session.delete(category)
        await self.session.flush()
        return category
