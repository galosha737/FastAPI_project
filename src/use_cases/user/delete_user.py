from infrastructure.postgres.repositories.user_rep import (
    UserRepository,)
from exceptions.user import UserNotFound


class DeleteUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user_id: int) -> None:
        user = await self.repository.get(user_id)
        if user is None:
            raise UserNotFound(user_id)
        
        await self.repository.delete(user)