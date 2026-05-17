from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....schems.user_s import UserCreate, UserUpdate
from ..models.user_m import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[User]:
        stmt = select(User).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def create(self, data: UserCreate) -> User:
        user = User(**data.model_dump(mode="json"))
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def update(self, user_id: int, data: UserUpdate) -> User | None:
        user = await self.get(user_id)
        if not user:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: int) -> User | None:
        user = await self.get(user_id)
        if not user:
            return None

        await self.session.delete(user)
        await self.session.flush()
        return user
