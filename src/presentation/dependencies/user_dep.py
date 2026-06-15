from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.postgres.database import get_db
from src.infrastructure.postgres.repositories.user_rep import UserRepository
from src.application.use_cases.user.create_user import CreateUserUseCase
from src.application.use_cases.user.update_user import UpdateUserUseCase
from src.application.use_cases.user.delete_user import DeleteUserUseCase
from src.application.use_cases.user.get_user import GetUserUseCase
from src.application.use_cases.user.get_list_user import GetUserListUseCase
from src.application.use_cases.user.change_user_role import ChangeUserRoleUseCase


DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_user_repository(session: DbSession) -> UserRepository:
    return UserRepository(session)


UserRepositoryDep = Annotated[UserRepository,
                              Depends(get_user_repository)]


def get_user_list_use_case(
    repository: UserRepositoryDep,
) -> GetUserListUseCase:
    return GetUserListUseCase(repository)


def get_user_use_case(
    repository: UserRepositoryDep,
) -> GetUserUseCase:
    return GetUserUseCase(repository)


def get_create_user_use_case(
    repository: UserRepositoryDep,
) -> CreateUserUseCase:
    return CreateUserUseCase(repository)


def get_update_user_use_case(
    repository: UserRepositoryDep,
) -> UpdateUserUseCase:
    return UpdateUserUseCase(repository)


def get_delete_user_use_case(
    repository: UserRepositoryDep,
) -> DeleteUserUseCase:
    return DeleteUserUseCase(repository)


def get_change_user_role_use_case(
    repository: UserRepositoryDep,
) -> ChangeUserRoleUseCase:
    return ChangeUserRoleUseCase(repository)


GetUserListUseCaseDep = Annotated[
    GetUserListUseCase,
    Depends(get_user_list_use_case),
]

GetUserUseCaseDep = Annotated[
    GetUserUseCase,
    Depends(get_user_use_case),
]

CreateUserUseCaseDep = Annotated[
    CreateUserUseCase,
    Depends(get_create_user_use_case),
]

UpdateUserUseCaseDep = Annotated[
    UpdateUserUseCase,
    Depends(get_update_user_use_case),
]

DeleteUserUseCaseDep = Annotated[
    DeleteUserUseCase,
    Depends(get_delete_user_use_case),
]

ChangeUserRoleUseCaseDep = Annotated[
    ChangeUserRoleUseCase,
    Depends(get_change_user_role_use_case),
]
