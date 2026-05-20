from infrastructure.postgres.models import User
from infrastructure.postgres.repositories.user_rep import (
    UserRepository,)
from schemas.user_s import UserCreate


class CreateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, data: UserCreate) -> User:
        user = User(
            username=data.username,
            password=data.password,
            email=data.email,
            bio_info=data.bio_info,
            first_name=data.first_name,
            last_name=data.last_name,
        )
        return await self.repository.create(user)