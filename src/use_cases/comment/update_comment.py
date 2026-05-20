from infrastructure.postgres.models import Comment
from infrastructure.postgres.repositories.comment_rep import (
    CommentRepository,)
from schemas.comment_s import CommentUpdate
from exceptions.comment import CommentNotFound


class UpdateCommentUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self,
                      comment_id: int,
                      data: CommentUpdate
                      ) -> Comment:
        comment = await self.repository.get(comment_id)
        if comment is None:
            raise CommentNotFound
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(comment, field, value)
        
        return await self.repository.update(comment)