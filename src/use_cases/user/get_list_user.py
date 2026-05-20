from infrastructure.postgres.models import User
from infrastructure.postgres.repositories.user_rep import (
    UserRepository,)


class GetUserListUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self,
                      *,
                      skip: int = 0,
                      limit: int = 10) -> list[User]:
        return await self.repository.get_list(skip=skip, limit=limit)
