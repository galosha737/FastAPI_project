from fastapi import HTTPException, status

from infrastructure.postgres.models import Location
from infrastructure.postgres.repositories.location_rep import (
    LocationRepository,)
from schemas.location_s import LocationCreate
from exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)


class CreateLocationUseCase:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    async def execute(self, data: LocationCreate) -> Location:
        name = data.name.strip()

        if not name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Location name cannot be empty",
            )
        
        location = Location(
            name=data.name,
            is_published=data.is_published,
        )
        try:
            return await self.repository.create(location)
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
