from fastapi import APIRouter
from starlette import status

from .dependencies.category_dep import (
    CreateCategoryUseCaseDep,
    DeleteCategoryUseCaseDep,
    GetCategoryListUseCaseDep,
    GetCategoryUseCaseDep,
    UpdateCategoryUseCaseDep,
)
from ..schemas.category_s import CategoryOut, CategoryUpdate, CategoryCreate


router = APIRouter(prefix='/categories', tags=['Категории'])


@router.get(
    "/",
    response_model=list[CategoryOut],
    status_code=status.HTTP_200_OK,
    summary="Категории:"
)
async def get_categories(
    use_case: GetCategoryListUseCaseDep,
    skip: int = 0,
    limit: int = 10,
):
    return await use_case.execute(skip=skip, limit=limit)


@router.get(
    "/{category_id}",
    response_model=CategoryOut,
    status_code=status.HTTP_200_OK,
    summary="Категория:"
)
async def get_category(
    use_case: GetCategoryUseCaseDep,
    category_id: int,
):
    return await use_case.execute(category_id)


@router.post(
    "/",
    response_model=CategoryOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать категорию:"
)
async def create_category(
    use_case: CreateCategoryUseCaseDep,
    category_in: CategoryCreate,
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
):
    await use_case.execute(category_id)
