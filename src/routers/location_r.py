from fastapi import APIRouter, HTTPException, Response
from starlette import status

from ..schemas.location_s import LocationOut, LocationUpdate, LocationCreate
from ..exceptions.location import LocationNotFound
from .dependencies.location_dep import (
    CreateLocationUseCaseDep,
    DeleteLocationUseCaseDep,
    GetLocationListUseCaseDep,
    GetLocationUseCaseDep,
    UpdateLocationUseCaseDep,
)


router = APIRouter(prefix='/locations', tags=['Местоположения'])


@router.get(
    "/",
    response_model=list[LocationOut],
    status_code=status.HTTP_200_OK,
    summary="Местоположение:"
)
async def get_locations(
    use_case: GetLocationListUseCaseDep,
    skip: int = 0,
    limit: int = 10,
):
    return await use_case.execute(skip=skip, limit=limit)


@router.get(
    "/{location_id}",
    response_model=LocationOut,
    status_code=status.HTTP_200_OK,
    summary="Местоположение:"
)
async def get_location(
    use_case: GetLocationUseCaseDep,
    location_id: int,
):
    try:
        return await use_case.execute(location_id)
    except LocationNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Местоположение не найдено!",
        ) from err


@router.post(
    "/",
    response_model=LocationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать местоположение:"
)
async def create_location(
    use_case: CreateLocationUseCaseDep,
    location_in: LocationCreate,
):
    return await use_case.execute(location_in)


@router.put(
    "/{location_id}",
    response_model=LocationOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить местоположение:"
)
async def update_location(
    use_case: UpdateLocationUseCaseDep,
    location_id: int,
    location_in: LocationUpdate,
):
    try:
        return await use_case.execute(location_id, location_in)
    except LocationNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Местоположение не найдено!",
        ) from err


@router.delete(
    "/{location_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить местоположение:"
)
async def delete_location(
    use_case: DeleteLocationUseCaseDep,
    location_id: int,
):
    try:
        await use_case.execute(location_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except LocationNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Местоположение не найдено!",
        ) from err
