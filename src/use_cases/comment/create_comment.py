from infrastructure.postgres.models import Comment
from infrastructure.postgres.repositories.comment_rep import (
    CommentRepository,)
from schemas.comment_s import CommentCreate


class CreateCommentUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self, data: CommentCreate) -> Comment:
        comment = Comment(
            text=data.text,
            author_id=data.author_id,
            post_id=data.post_id,
        )
        return await self.repository.create(comment)