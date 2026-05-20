from infrastructure.postgres.models import Comment
from infrastructure.postgres.repositories.comment_rep import (
    CommentRepository,)
from exceptions.comment import CommentNotFound


class GetCommentUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self, comment_id: int) -> Comment:
        comment = await self.repository.get(comment_id)
        if comment is None:
            raise CommentNotFound(comment_id)
        return comment
