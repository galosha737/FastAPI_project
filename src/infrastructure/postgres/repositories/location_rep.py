from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.location_m import Location
from src.exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)


class LocationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[Location]:
        try:
            s = select(Location).offset(skip).limit(limit)
            result = await self.session.execute(s)
            return list(result.scalars().all())
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Location",
                operation="get_list",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Location",
                operation="get_list",
                details=str(err),
            ) from err

    async def get(self, location_id: int) -> Location | None:
        try:
            return await self.session.get(Location, location_id)
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Location",
                operation="get",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Location",
                operation="get",
                details=str(err),
            ) from err

    async def create(self, location: Location) -> Location:
        try:
            self.session.add(location)
            await self.session.flush()
            await self.session.refresh(location)
            return location
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="create",
                obj=location,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Location",
                operation="create",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Location",
                operation="create",
                details=str(err),
            ) from err

    async def update(self, location: Location) -> Location:
        try:
            await self.session.flush()
            await self.session.refresh(location)
            return location
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="update",
                obj=location,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Location",
                operation="update",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Location",
                operation="update",
                details=str(err),
            ) from err

    async def delete(self, location: Location) -> None:
        try:
            await self.session.delete(location)
            await self.session.flush()
            return None
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="delete",
                obj=location,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Location",
                operation="delete",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Location",
                operation="delete",
                details=str(err),
            ) from err

    def _map_integrity_error(
        self,
        *,
        err: IntegrityError,
        operation: str,
        obj: Location,
    ) -> DatabaseError:
        message = str(err.orig).lower()

        if "unique" in message or "duplicate" in message:
            return DataConflictError(
                entity="Location",
                operation=operation,
                field="name",
                value=getattr(obj, "name", None),
                details=str(err.orig),
            )

        if "foreign key" in message:
            return ForeignKeyConflictError(
                entity="Location",
                operation=operation,
                details=str(err.orig),
            )

        return DatabaseError(
            entity="Location",
            operation=operation,
            details=str(err.orig),
        )

    async def get_list_published(self,
                                 skip: int = 0,
                                 limit: int = 10) -> list[Location]:
        try:
            s = select(Location).where(Location.is_published).offset(skip).limit(limit)
            result = await self.session.execute(s)
            return list(result.scalars().all())
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Location",
                operation="get_list_published",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Location",
                operation="get_list_published",
                details=str(err),
            ) from err
        
    async def get_published(self,
                            location_id: int) -> Location | None:
        try:
            s = select(Location).where(Location.id == location_id, Location.is_published)
            result = await self.session.execute(s)
            return result.scalar_one_or_none()
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Location",
                operation="get_published",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Location",
                operation="get_published",
                details=str(err),
            ) from err
