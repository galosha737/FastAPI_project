from fastapi import HTTPException, status

from src.domain.exceptions.database import (
    DatabaseError,
    DatabaseUnavailableError,
)
from src.infrastructure.postgres.models import Location, User
from src.infrastructure.postgres.repositories.location_rep import LocationRepository


class GetLocationUseCase:
    def __init__(self, repository: LocationRepository):
        self.repository = repository

    async def execute(self, location_id: int, current_user: User) -> Location:
        try:
            if location_id <= 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="location_id must be greater than 0",
                )
            
            if current_user.role in ["admin", "super_admin"]:
                location = await self.repository.get(location_id)
            else:
                location = await self.repository.get_published(location_id)
            if location is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Location with id={location_id} not found",
                )

            return location
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
