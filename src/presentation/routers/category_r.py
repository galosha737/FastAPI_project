from typing import Annotated
from fastapi import APIRouter, Depends
from starlette import status

from ..dependencies.category_dep import (
    CreateCategoryUseCaseDep,
    DeleteCategoryUseCaseDep,
    GetCategoryListUseCaseDep,
    GetCategoryUseCaseDep,
    UpdateCategoryUseCaseDep,
)
from ..schemas.category_s import CategoryOut, CategoryUpdate, CategoryCreate
from ..dependencies.auth_dep import get_current_user, get_admin_user
from src.infrastructure.postgres.models.user_m import User


router = APIRouter(prefix='/categories', tags=['Категории'])


@router.get(
    "/",
    response_model=list[CategoryOut],
    status_code=status.HTTP_200_OK,
    summary="Категории:"
)
async def get_categories(
    use_case: GetCategoryListUseCaseDep,
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
):
    return await use_case.execute(skip=skip, limit=limit, current_user=current_user)


@router.get(
    "/{category_id}",
    response_model=CategoryOut,
    status_code=status.HTTP_200_OK,
    summary="Категория:"
)
async def get_category(
    use_case: GetCategoryUseCaseDep,
    category_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await use_case.execute(category_id, current_user=current_user)


@router.post(
    "/",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать категорию:"
)
async def create_category(
    use_case: CreateCategoryUseCaseDep,
    category_in: CategoryCreate,
    current_admin: Annotated[User, Depends(get_admin_user)]
):
    return await use_case.execute(category_in)


@router.put(
    "/{category_id}",
    response_model=CategoryOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить категорию:"
)
async def update_category(
    use_case: UpdateCategoryUseCaseDep,
    category_id: int,
    category_in: CategoryUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    current_admin: Annotated[User, Depends(get_admin_user)]
):
    return await use_case.execute(category_id, category_in)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить категорию:"
)
async def delete_category(
    use_case: DeleteCategoryUseCaseDep,
    category_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    current_admin: Annotated[User, Depends(get_admin_user)]
):
    await use_case.execute(category_id)
