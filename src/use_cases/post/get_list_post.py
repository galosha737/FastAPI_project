from infrastructure.postgres.models import Post
from infrastructure.postgres.repositories.post_rep import (
    PostRepository,)


class GetPostListUseCase:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def execute(self,
                      *,
                      skip: int = 0,
                      limit: int = 10) -> list[Post]:
        return await self.repository.get_list(skip=skip, limit=limit)
