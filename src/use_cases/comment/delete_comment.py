from infrastructure.postgres.repositories.comment_rep import (
    CommentRepository,)
from exceptions.comment import CommentNotFound


class DeleteCommentUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self, comment_id: int) -> None:
        comment = await self.repository.get(comment_id)
        if comment is None:
            raise CommentNotFound(comment_id)
        
        await self.repository.delete(comment)