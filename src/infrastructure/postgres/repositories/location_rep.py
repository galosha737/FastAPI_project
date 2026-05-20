from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.location_m import Location


class LocationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[Location]:
        s = select(Location).offset(skip).limit(limit)
        result = await self.session.execute(s)
        return list(result.scalars().all())

    async def get(self, Location_id: int) -> Location | None:
        return await self.session.get(Location, Location_id)

    async def create(self, location: Location) -> Location:
        self.session.add(location)
        await self.session.flush()
        await self.session.refresh(location)
        return location

    async def update(self, location: Location) -> Location:
        await self.session.flush()
        await self.session.refresh(location)
        return location

    async def delete(self, location: Location) -> None:
        await self.session.delete(location)
        await self.session.flush()
        return None
