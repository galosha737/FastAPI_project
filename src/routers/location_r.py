from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..infrastructure.postgres.database import get_db
from ..infrastructure.postgres.repositories.location_rep import (
    LocationRepository)
from ..schems.location_s import LocationOut, LocationUpdateAndCreate


router = APIRouter(prefix='/locations', tags=['Местоположения'])


def get_location_repository(
        session: AsyncSession = Depends(get_db)
        ) -> LocationRepository:
    return LocationRepository(session)


@router.get(
    "/",
    response_model=list[LocationOut],
    status_code=status.HTTP_200_OK,
    summary="Местоположение:"
)
async def get_locations(
    skip: int = 0,
    limit: int = 10,
    repository: LocationRepository = Depends(get_location_repository),
):
    return await repository.get_list(skip=skip, limit=limit)


@router.get(
    "/{location_id}",
    response_model=LocationOut,
    status_code=status.HTTP_200_OK,
    summary="Местоположение:"
)
async def get_location(
    location_id: int,
    repository: LocationRepository = Depends(get_location_repository),
):
    location = await repository.get(location_id)
    if not location:
        raise HTTPException(status_code=404,
                            detail="Местоположение не найдено!")
    return location


@router.post(
    "/create",
    response_model=LocationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать местоположение:"
)
async def create_location(
    location_in: LocationUpdateAndCreate,
    repository: LocationRepository = Depends(get_location_repository),
):
    return await repository.create(location_in)


@router.put(
    "/put/{location_id}",
    response_model=LocationOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить местоположение:"
)
async def update_location(
    location_id: int,
    location_in: LocationUpdateAndCreate,
    repository: LocationRepository = Depends(get_location_repository),
):
    location = await repository.update(location_id, location_in)
    if not location:
        raise HTTPException(status_code=404,
                            detail="Местоположение не найдено!")
    return location


@router.delete(
    "/delete/{location_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить местоположение:"
)
async def delete_location(
    location_id: int,
    repository: LocationRepository = Depends(get_location_repository),
):
    location = await repository.delete(location_id)
    if not location:
        raise HTTPException(status_code=404,
                            detail="Местоположение не найдено!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
