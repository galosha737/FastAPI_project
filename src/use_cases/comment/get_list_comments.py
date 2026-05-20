from infrastructure.postgres.models import Comment
from infrastructure.postgres.repositories.comment_rep import (
    CommentRepository,)


class GetCommentListUseCase:
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def execute(self,
                      *,
                      skip: int = 0,
                      limit: int = 10) -> list[Comment]:
        return await self.repository.get_list(skip=skip, limit=limit)
