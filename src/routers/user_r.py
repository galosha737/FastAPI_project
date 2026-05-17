from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..infrastructure.postgres.database import get_db
from ..infrastructure.postgres.repositories.user_rep import UserRepository
from ..schems.user_s import UserUpdate, UserCreate, UserOut


router = APIRouter(prefix='/users', tags=['Пользователи'])


def get_user_repository(
        session: AsyncSession = Depends(get_db)
        ) -> UserRepository:
    return UserRepository(session)


@router.get(
    "/",
    response_model=list[UserOut],
    status_code=status.HTTP_200_OK,
    summary="Пользователи:"
)
async def get_users(
    skip: int = 0,
    limit: int = 10,
    repository: UserRepository = Depends(get_user_repository),
):
    return await repository.get_list(skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Пользователь:"
)
async def get_user(
    user_id: int,
    repository: UserRepository = Depends(get_user_repository),
):
    user = await repository.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    return user


@router.post(
    "/create",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать пользователя:"
)
async def create_user(
        user_in: UserCreate,
        repository: UserRepository = Depends(get_user_repository),
):
    return await repository.create(user_in)


@router.put(
    "/put/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить пользователя:"
)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    repository: UserRepository = Depends(get_user_repository),
):
    user = await repository.update(user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    return user


@router.delete(
    "/delete/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя:"
)
async def delete_user(
    user_id: int,
    repository: UserRepository = Depends(get_user_repository),
):
    user = await repository.delete(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
