from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ....schems.post_s import PostCreate, PostUpdate
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

    async def create(self, data: PostCreate) -> Post:
        post = Post(**data.model_dump())
        self.session.add(post)
        await self.session.flush()
        await self.session.refresh(post)
        return post

    async def update(self,
                     post_id: int,
                     data: PostUpdate) -> Post | None:
        post = await self.get(post_id)
        if not post:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(post, field, value)

        await self.session.flush()
        await self.session.refresh(post)
        return post

    async def delete(self, post_id: int) -> Post | None:
        post = await self.get(post_id)
        if not post:
            return None

        await self.session.delete(post)
        await self.session.flush()
        return post
