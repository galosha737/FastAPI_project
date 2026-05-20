from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.postgres.database import get_db
from infrastructure.postgres.repositories.post_rep import PostRepository
from use_cases.post.create_post import CreatePostUseCase
from use_cases.post.update_post import UpdatePostUseCase
from use_cases.post.delete_post import DeletePostUseCase
from use_cases.post.get_post import GetPostUseCase
from use_cases.post.get_list_post import GetPostListUseCase


DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_post_repository(session: DbSession) -> PostRepository:
    return PostRepository(session)


PostRepositoryDep = Annotated[PostRepository,
                              Depends(get_post_repository)]


def get_post_list_use_case(
    repository: PostRepositoryDep,
) -> GetPostListUseCase:
    return GetPostListUseCase(repository)


def get_post_use_case(
    repository: PostRepositoryDep,
) -> GetPostUseCase:
    return GetPostUseCase(repository)


def get_create_post_use_case(
    repository: PostRepositoryDep,
) -> CreatePostUseCase:
    return CreatePostUseCase(repository)


def get_update_post_use_case(
    repository: PostRepositoryDep,
) -> UpdatePostUseCase:
    return UpdatePostUseCase(repository)


def get_delete_post_use_case(
    repository: PostRepositoryDep,
) -> DeletePostUseCase:
    return DeletePostUseCase(repository)


GetPostListUseCaseDep = Annotated[
    GetPostListUseCase,
    Depends(get_post_list_use_case),
]

GetPostUseCaseDep = Annotated[
    GetPostUseCase,
    Depends(get_post_use_case),
]

CreatePostUseCaseDep = Annotated[
    CreatePostUseCase,
    Depends(get_create_post_use_case),
]

UpdatePostUseCaseDep = Annotated[
    UpdatePostUseCase,
    Depends(get_update_post_use_case),
]

DeletePostUseCaseDep = Annotated[
    DeletePostUseCase,
    Depends(get_delete_post_use_case),
]
