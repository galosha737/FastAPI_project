from infrastructure.postgres.models import User
from infrastructure.postgres.repositories.user_rep import (
    UserRepository,)
from schemas.user_s import UserUpdate
from exceptions.user import UserNotFound


class UpdateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self,
                      user_id: int,
                      data: UserUpdate
                      ) -> User:
        user = await self.repository.get(user_id)
        if user is None:
            raise UserNotFound
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(user, field, value)
        
        return await self.repository.update(user)
