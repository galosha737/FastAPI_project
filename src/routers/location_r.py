from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from starlette import status
from src.infrastructure.sqlite.database import get_db
from src.repositories.location_rep import LocationRepository
from src.schems.location_s import LocationOut, LocationUpdateAndCreate


router = APIRouter(prefix='/locations', tags=['Местоположения'])

def get_location_repository(session: Session = Depends(get_db)) -> LocationRepository:
    return LocationRepository(session)

@router.get(
    "/",
    response_model=List[LocationOut],
    status_code=status.HTTP_200_OK,
    summary="Местоположение:"
)
def get_locations(
    skip: int = 0,
    limit: int = 10,
    repository: LocationRepository = Depends(get_location_repository),
):
    return repository.get_list(skip=skip, limit=limit)

@router.get(
    "/{location_id}",
    response_model=LocationOut,
    status_code=status.HTTP_200_OK,
    summary="Местоположение:"
)
def get_location(
    location_id: int,
    repository: LocationRepository = Depends(get_location_repository),
):
    location = repository.get(location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Местоположение не найдено")
    return location

@router.post(
    "/create",
    response_model=LocationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать местоположение:"
)
def create_location(
    location_in: LocationUpdateAndCreate,
    repository: LocationRepository = Depends(get_location_repository),
):
    return repository.create(location_in)

@router.put(
    "/put/{location_id}",
    response_model=LocationOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить местоположение:"
)
def update_location(
    location_id: int,
    location_in: LocationUpdateAndCreate,
    repository: LocationRepository = Depends(get_location_repository),
):
    location = repository.update(location_id, location_in)
    if not location:
        raise HTTPException(status_code=404, detail="Местоположение не найдено")
    return location

@router.delete(
    "/delete/{location_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить местоположение:"
)
def delete_location(
    location_id: int,
    repository: LocationRepository = Depends(get_location_repository),
):
    location = repository.delete(location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Местоположение не найдено")
    return None