from infrastructure.postgres.repositories.post_rep import (
    PostRepository,)
from exceptions.post import PostNotFound


class DeletePostUseCase:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def execute(self, post_id: int) -> None:
        post = await self.repository.get(post_id)
        if post is None:
            raise PostNotFound(post_id)
        
        await self.repository.delete(post)