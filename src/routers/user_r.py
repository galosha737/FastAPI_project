from fastapi import APIRouter
from starlette import status

from ..schemas.user_s import UserCreate, UserOut, UserUpdate
from .dependencies.user_dep import (
    CreateUserUseCaseDep,
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


@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать пользователя:"
)
async def create_user(
    use_case: CreateUserUseCaseDep,
    user_in: UserCreate,
):
    return await use_case.execute(user_in)


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
):
    return await use_case.execute(user_id, user_in)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя:"
)
async def delete_user(
    use_case: DeleteUserUseCaseDep,
    user_id: int,
):
    await use_case.execute(user_id)
