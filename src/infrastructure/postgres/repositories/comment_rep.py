from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.comment_m import Comment
from ....schems.comment_s import CommentUpdate, CommentCreate


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[Comment]:
        s = select(Comment).offset(skip).limit(limit)
        result = await self.session.execute(s)
        return list(result.scalars().all())

    async def get(self, Comment_id: int) -> Comment | None:
        return await self.session.get(Comment, Comment_id)

    async def create(self, data: CommentCreate) -> Comment:
        comment = Comment(**data.model_dump())
        self.session.add(comment)
        await self.session.flush()
        await self.session.refresh(comment)
        return comment

    async def update(self,
                     comment_id: int,
                     data: CommentUpdate) -> Comment | None:
        comment = await self.get(comment_id)
        if not comment:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(comment, field, value)

        await self.session.flush()
        await self.session.refresh(comment)
        return comment

    async def delete(self, comment_id: int) -> Comment | None:
        comment = await self.get(comment_id)
        if not comment:
            return None

        await self.session.delete(comment)
        await self.session.flush()
        return comment
