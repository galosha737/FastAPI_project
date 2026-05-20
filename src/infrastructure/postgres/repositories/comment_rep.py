from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.comment_m import Comment


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[Comment]:
        s = select(Comment).offset(skip).limit(limit)
        result = await self.session.execute(s)
        return list(result.scalars().all())

    async def get(self, Comment_id: int) -> Comment | None:
        return await self.session.get(Comment, Comment_id)

    async def create(self, comment: Comment) -> Comment:
        self.session.add(comment)
        await self.session.flush()
        await self.session.refresh(comment)
        return comment

    async def update(self, comment: Comment) -> Comment:
        await self.session.flush()
        await self.session.refresh(comment)
        return comment

    async def delete(self, comment: Comment) -> None:
        await self.session.delete(comment)
        await self.session.flush()
        return None
