from infrastructure.postgres.repositories.location_rep import (
    LocationRepository,)
from exceptions.location import LocationNotFound


class DeleteLocationUseCase:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    async def execute(self, location_id: int) -> None:
        location = await self.repository.get(location_id)
        if location is None:
            raise LocationNotFound(location_id)
        
        await self.repository.delete(location)