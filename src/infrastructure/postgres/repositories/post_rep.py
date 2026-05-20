from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.post_m import Post


class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[Post]:
        s = select(Post).offset(skip).limit(limit)
        result = await self.session.execute(s)
        return list(result.scalars().all())

    async def get(self, Post_id: int) -> Post | None:
        return await self.session.get(Post, Post_id)

    async def create(self, post: Post) -> Post:
        self.session.add(post)
        await self.session.flush()
        await self.session.refresh(post)
        return post

    async def update(self, post: Post) -> Post:
        await self.session.flush()
        await self.session.refresh(post)
        return post

    async def delete(self, post: Post) -> None:
        await self.session.delete(post)
        await self.session.flush()
        return None
