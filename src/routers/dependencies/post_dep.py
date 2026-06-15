from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.postgres.database import get_db
from src.infrastructure.postgres.repositories.post_rep import PostRepository
from src.use_cases.post.create_post import CreatePostUseCase
from src.use_cases.post.update_post import UpdatePostUseCase
from src.use_cases.post.delete_post import DeletePostUseCase
from src.use_cases.post.get_post import GetPostUseCase
from src.use_cases.post.get_list_post import GetPostListUseCase
from src.use_cases.file_use_case import FileUseCase
from src.infrastructure.postgres.repositories.file_rep import FileRepository


DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_post_repository(session: DbSession) -> PostRepository:
    return PostRepository(session)


PostRepositoryDep = Annotated[PostRepository,
                              Depends(get_post_repository)]


def get_file_repository(session: DbSession) -> FileRepository:
    return FileRepository(session)


FileRepositoryDep = Annotated[
    FileRepository,
    Depends(get_file_repository)
]


def get_file_use_case(
    repository: FileRepositoryDep,
) -> FileUseCase:
    return FileUseCase(repository)


FileUseCaseDep = Annotated[
    FileUseCase,
    Depends(get_file_use_case),
]


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
    file_use_case: FileUseCaseDep
) -> CreatePostUseCase:
    return CreatePostUseCase(repository, file_use_case)


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
