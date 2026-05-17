from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..models.location_m import Location
from ....schems.location_s import LocationUpdateAndCreate


class LocationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[Location]:
        s = select(Location).offset(skip).limit(limit)
        result = await self.session.execute(s)
        return list(result.scalars().all())

    async def get(self, Location_id: int) -> Location | None:
        return await self.session.get(Location, Location_id)

    async def create(self, data: LocationUpdateAndCreate) -> Location:
        location = Location(**data.model_dump())
        self.session.add(location)
        await self.session.flush()
        await self.session.refresh(location)
        return location

    async def update(self,
                     location_id: int,
                     data: LocationUpdateAndCreate) -> Location | None:
        location = await self.get(location_id)
        if not location:
            return None

        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(location, field, value)

        await self.session.flush()
        await self.session.refresh(location)
        return location

    async def delete(self, location_id: int) -> Location | None:
        location = await self.get(location_id)
        if not location:
            return None

        await self.session.delete(location)
        await self.session.flush()
        return location
