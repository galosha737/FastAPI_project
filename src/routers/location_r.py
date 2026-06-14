from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status

from src.infrastructure.postgres.models.user_m import User
from .dependencies.auth_dep import get_admin_user, get_current_user
from ..schemas.location_s import LocationOut, LocationUpdate, LocationCreate
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
    summary="Местоположения:"
)
async def get_locations(
    use_case: GetLocationListUseCaseDep,
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
):
    return await use_case.execute(skip=skip, limit=limit, current_user=current_user)


@router.get(
    "/{location_id}",
    response_model=LocationOut,
    status_code=status.HTTP_200_OK,
    summary="Местоположение:"
)
async def get_location(
    use_case: GetLocationUseCaseDep,
    current_user: Annotated[User, Depends(get_current_user)],
    location_id: int,
):
    return await use_case.execute(location_id, current_user)


@router.post(
    "/",
    response_model=LocationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать местоположение:"
)
async def create_location(
    use_case: CreateLocationUseCaseDep,
    location_in: LocationCreate,
    current_admin: Annotated[User, Depends(get_admin_user)]
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
    current_admin: Annotated[User, Depends(get_admin_user)]
):
    return await use_case.execute(location_id, location_in)


@router.delete(
    "/{location_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить местоположение:"
)
async def delete_location(
    use_case: DeleteLocationUseCaseDep,
    location_id: int,
    current_admin: Annotated[User, Depends(get_admin_user)]

):
    await use_case.execute(location_id)
