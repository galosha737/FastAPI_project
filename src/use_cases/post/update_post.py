from infrastructure.postgres.models import Post
from infrastructure.postgres.repositories.post_rep import (
    PostRepository,)
from schemas.post_s import PostUpdate
from exceptions.post import PostNotFound


class UpdatePostUseCase:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def execute(self,
                      post_id: int,
                      data: PostUpdate
                      ) -> Post:
        post = await self.repository.get(post_id)
        if post is None:
            raise PostNotFound
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(post, field, value)
        
        return await self.repository.update(post)
