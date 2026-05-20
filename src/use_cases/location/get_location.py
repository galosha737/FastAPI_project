from infrastructure.postgres.models import Location
from infrastructure.postgres.repositories.location_rep import (
    LocationRepository,)
from exceptions.location import LocationNotFound


class GetLocationUseCase:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    async def execute(self, location_id: int) -> Location:
        location = await self.repository.get(location_id)
        if location is None:
            raise LocationNotFound(location_id)
        return location
