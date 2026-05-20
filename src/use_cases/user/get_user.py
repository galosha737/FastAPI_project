from infrastructure.postgres.models import User
from infrastructure.postgres.repositories.user_rep import (
    UserRepository,)
from exceptions.user import UserNotFound


class GetUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> User:
        user = await self.repository.get(user_id)
        if user is None:
            raise UserNotFound(user_id)
        return user
