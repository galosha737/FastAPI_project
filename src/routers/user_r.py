from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status

from src.infrastructure.postgres.models.user_m import User
from .dependencies.auth_dep import get_current_user
from ..schemas.user_s import UserOut, UserUpdate
from .dependencies.user_dep import (
    DeleteUserUseCaseDep,
    GetUserListUseCaseDep,
    GetUserUseCaseDep,
    UpdateUserUseCaseDep,
)


router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get(
    "/",
    response_model=list[UserOut],
    status_code=status.HTTP_200_OK,
    summary="Пользователи:"
)
async def get_users(
    use_case: GetUserListUseCaseDep,
    skip: int = 0,
    limit: int = 10,
):
    return await use_case.execute(skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Пользователь:"
)
async def get_user(
    use_case: GetUserUseCaseDep,
    user_id: int,
):
    return await use_case.execute(user_id)


@router.put(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить пользователя:"
)
async def update_user(
    use_case: UpdateUserUseCaseDep,
    user_id: int,
    user_in: UserUpdate,
    current_user: Annotated[User, Depends(get_current_user)]
):
    return await use_case.execute(user_id, user_in, current_user)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя:"
)
async def delete_user(
    use_case: DeleteUserUseCaseDep,
    user_id: int,
    current_user: Annotated[User, Depends(get_current_user)]
):
    await use_case.execute(user_id, current_user)
