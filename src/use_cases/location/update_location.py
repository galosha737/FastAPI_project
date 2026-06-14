from fastapi import HTTPException, status

from src.exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)
from src.infrastructure.postgres.models import Location
from src.infrastructure.postgres.repositories.location_rep import (
    LocationRepository,)
from src.schemas.location_s import LocationUpdate


class UpdateLocationUseCase:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    async def execute(self,
                      location_id: int,
                      data: LocationUpdate
                      ) -> Location:
        location = await self.repository.get(location_id)
        if location is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Location with id={location_id} not found",
            )
        try:
            update_data = data.model_dump(exclude_unset=True)

            for field, value in update_data.items():
                setattr(location, field, value)
        
            return await self.repository.update(location)
        except DataConflictError as err:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(err),
            ) from err
        except ForeignKeyConflictError as err:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=str(err),
            ) from err
        except DatabaseUnavailableError as err:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=str(err),
            ) from err
        except DatabaseError as err:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(err),
            ) from err
