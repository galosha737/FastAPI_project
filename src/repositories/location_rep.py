from sqlalchemy.orm import Session
from ..infrastructure.sqlite.models import Location
from ..schems.location_s import LocationUpdateAndCreate
from typing import List, Optional


class LocationRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_list(self, skip: int = 0, limit: int = 10) -> List[Location]:
        location_list = self.session.query(Location).offset(skip).limit(limit).all()
        return location_list # type: ignore

    def get(self, location_id: int) -> Optional[Location]:
        return self.session.get(Location, location_id)

    def create(self, data: LocationUpdateAndCreate) -> Location:
        location = Location(**data.model_dump()) # type: ignore
        self.session.add(location)
        self.session.commit()
        self.session.refresh(location)
        return location

    def update(self, location_id: int, data: LocationUpdateAndCreate) -> Optional[Location]:
        location = self.get(location_id)
        if not location:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(location, field, value)
        self.session.commit()
        self.session.refresh(location)
        return location

    def delete(self, location_id: int) -> Optional[Location]:
        location = self.get(location_id)
        if not location:
            return None
        self.session.delete(location)
        self.session.commit()
        return location