from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from starlette import status
from ..infrastructure.sqlite.database import get_db
from ..repositories.user_rep import UserRepository
from ..schems.user_s import UserUpdate, UserCreate, UserOut


router = APIRouter(prefix='/users', tags=['Пользователь'])

def get_user_repository(session: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(session)

@router.get(
    "/",
    response_model=List[UserOut],
    status_code=status.HTTP_200_OK,
    summary="Пользователи:"
)
def get_users(
    skip: int = 0,
    limit: int = 10,
    repository: UserRepository = Depends(get_user_repository),
):
    return repository.get_list(skip=skip, limit=limit)

@router.get(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Пользователь:"
)
def get_user(
    user_id: int,
    repository: UserRepository = Depends(get_user_repository),
):
    user = repository.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    return user


@router.post(
    "/create",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать пользователя:"
)
def create_user(
        user_in: UserCreate,
        repository: UserRepository = Depends(get_user_repository),
):
    return repository.create(user_in)

@router.put(
    "/put/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить пользователя:"
)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    repository: UserRepository = Depends(get_user_repository),
):
    user = repository.update(user_id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.delete(
    "/delete/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя:"
)
def delete_user(
    user_id: int,
    repository: UserRepository = Depends(get_user_repository),
):
    user = repository.delete(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найдено")
    return None