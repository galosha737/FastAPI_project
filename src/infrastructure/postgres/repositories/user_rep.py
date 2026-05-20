from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user_m import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[User]:
        s = select(User).offset(skip).limit(limit)
        result = await self.session.execute(s)
        return list(result.scalars().all())

    async def get(self, User_id: int) -> User | None:
        return await self.session.get(User, User_id)

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def update(self, user: User) -> User:
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.flush()
        return None
