from infrastructure.postgres.models import Location
from infrastructure.postgres.repositories.location_rep import (
    LocationRepository,)


class GetLocationListUseCase:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    async def execute(self,
                      *,
                      skip: int = 0,
                      limit: int = 10) -> list[Location]:
        return await self.repository.get_list(skip=skip, limit=limit)
