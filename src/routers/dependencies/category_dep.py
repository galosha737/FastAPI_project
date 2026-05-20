from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.postgres.database import get_db
from infrastructure.postgres.repositories.category_rep import CategoryRepository
from use_cases.category.create_category import CreateCategoryUseCase
from use_cases.category.update_category import UpdateCategoryUseCase
from use_cases.category.delete_category import DeleteCategoryUseCase
from use_cases.category.get_category import GetCategoryUseCase
from use_cases.category.get_list_categories import GetCategoryListUseCase


DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_category_repository(session: DbSession) -> CategoryRepository:
    return CategoryRepository(session)


CategoryRepositoryDep = Annotated[CategoryRepository,
                                  Depends(get_category_repository)]


def get_category_list_use_case(
    repository: CategoryRepositoryDep,
) -> GetCategoryListUseCase:
    return GetCategoryListUseCase(repository)


def get_category_use_case(
    repository: CategoryRepositoryDep,
) -> GetCategoryUseCase:
    return GetCategoryUseCase(repository)


def get_create_category_use_case(
    repository: CategoryRepositoryDep,
) -> CreateCategoryUseCase:
    return CreateCategoryUseCase(repository)


def get_update_category_use_case(
    repository: CategoryRepositoryDep,
) -> UpdateCategoryUseCase:
    return UpdateCategoryUseCase(repository)


def get_delete_category_use_case(
    repository: CategoryRepositoryDep,
) -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase(repository)


GetCategoryListUseCaseDep = Annotated[
    GetCategoryListUseCase,
    Depends(get_category_list_use_case),
]

GetCategoryUseCaseDep = Annotated[
    GetCategoryUseCase,
    Depends(get_category_use_case),
]

CreateCategoryUseCaseDep = Annotated[
    CreateCategoryUseCase,
    Depends(get_create_category_use_case),
]

UpdateCategoryUseCaseDep = Annotated[
    UpdateCategoryUseCase,
    Depends(get_update_category_use_case),
]

DeleteCategoryUseCaseDep = Annotated[
    DeleteCategoryUseCase,
    Depends(get_delete_category_use_case),
]