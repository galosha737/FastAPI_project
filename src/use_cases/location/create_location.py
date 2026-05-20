from infrastructure.postgres.models import Location
from infrastructure.postgres.repositories.location_rep import (
    LocationRepository,)
from schemas.location_s import LocationCreate


class CreateLocationUseCase:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    async def execute(self, data: LocationCreate) -> Location:
        location = Location(
            name=data.name,
            is_published=data.is_published,
        )
        return await self.repository.create(location)