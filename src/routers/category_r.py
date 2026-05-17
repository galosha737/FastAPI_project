from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..infrastructure.postgres.database import get_db
from ..infrastructure.postgres.repositories.category_rep import (
    CategoryRepository,
)
from ..schems.category_s import CategoryOut, CategoryUpdateAndCreate

router = APIRouter(prefix='/categories', tags=['Категории'])


DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_category_repository(session: DbSession) -> CategoryRepository:
    return CategoryRepository(session)


CategoryRepositoryDep = Annotated[CategoryRepository,
                                  Depends(get_category_repository)]


@router.get(
    "/",
    response_model=list[CategoryOut],
    status_code=status.HTTP_200_OK,
    summary="Категории:"
)
async def get_categories(
    repository: CategoryRepositoryDep,
    skip: int = 0,
    limit: int = 10,
):
    return await repository.get_list(skip=skip, limit=limit)


@router.get(
    "/{category_id}",
    response_model=CategoryOut,
    status_code=status.HTTP_200_OK,
    summary="Категория:"
)
async def get_category(
    repository: CategoryRepositoryDep,
    category_id: int,
):
    category = await repository.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена!")
    return category


@router.post(
    "/create",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать категорию:"
)
async def create_category(
    repository: CategoryRepositoryDep,
    category_in: CategoryUpdateAndCreate,
):
    return await repository.create(category_in)


@router.put(
    "/put/{category_id}",
    response_model=CategoryOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить категорию:"
)
async def update_category(
    repository: CategoryRepositoryDep,
    category_id: int,
    category_in: CategoryUpdateAndCreate,
):
    category = await repository.update(category_id, category_in)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


@router.delete(
    "/delete/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить категорию:"
)
async def delete_category(
    repository: CategoryRepositoryDep,
    category_id: int,
):
    category = await repository.delete(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
