from infrastructure.postgres.models import Post
from infrastructure.postgres.repositories.post_rep import (
    PostRepository,)
from schemas.post_s import PostCreate


class CreatePostUseCase:
    def __init__(self, repository: PostRepository):
        self.repository = repository

    async def execute(self, data: PostCreate) -> Post:
        post = Post(
            title=data.title,
            is_published=data.is_published,
            text=data.text,
            image=data.image,
            category_id=data.category_id,
            location_id=data.location_id,
            author_id=data.author_id,
        )
        return await self.repository.create(post)