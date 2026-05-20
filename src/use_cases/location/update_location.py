from infrastructure.postgres.models import Location
from infrastructure.postgres.repositories.location_rep import (
    LocationRepository,)
from schemas.location_s import LocationUpdate
from exceptions.location import LocationNotFound


class UpdateLocationUseCase:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    async def execute(self,
                      location_id: int,
                      data: LocationUpdate
                      ) -> Location:
        location = await self.repository.get(location_id)
        if location is None:
            raise LocationNotFound
        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(location, field, value)
        
        return await self.repository.update(location)
