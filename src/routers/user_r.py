from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..infrastructure.postgres.database import get_db
from ..infrastructure.postgres.repositories.user_rep import UserRepository
from ..schems.user_s import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix='/users', tags=['Пользователи'])

# в DbSession кладем AsyncSession, которую берем из get_db
DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_user_repository(session: DbSession) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


@router.get(
    "/",
    response_model=list[UserOut],
    status_code=status.HTTP_200_OK,
    summary="Пользователи:"
)
async def get_users(
    repository: UserRepositoryDep,
    skip: int = 0,
    limit: int = 10,
):
    return await repository.get_list(skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Пользователь:"
)
async def get_user(
    repository: UserRepositoryDep,
    user_id: int,
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
    repository: UserRepositoryDep,
    user_in: UserCreate,
):
    return await repository.create(user_in)


@router.put(
    "/put/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить пользователя:"
)
async def update_user(
    repository: UserRepositoryDep,
    user_id: int,
    user_in: UserUpdate,
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
    repository: UserRepositoryDep,
    user_id: int,
):
    user = await repository.delete(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
