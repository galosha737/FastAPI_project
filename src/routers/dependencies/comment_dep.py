from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.postgres.database import get_db
from src.infrastructure.postgres.repositories.comment_rep import CommentRepository
from src.use_cases.comment.create_comment import CreateCommentUseCase
from src.use_cases.comment.update_comment import UpdateCommentUseCase
from src.use_cases.comment.delete_comment import DeleteCommentUseCase
from src.use_cases.comment.get_comment import GetCommentUseCase
from src.use_cases.comment.get_list_comments import GetCommentListUseCase
from .post_dep import FileUseCaseDep


DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_comment_repository(session: DbSession) -> CommentRepository:
    return CommentRepository(session)


CommentRepositoryDep = Annotated[CommentRepository,
                                  Depends(get_comment_repository)]


def get_comment_list_use_case(
    repository: CommentRepositoryDep,
) -> GetCommentListUseCase:
    return GetCommentListUseCase(repository)


def get_comment_use_case(
    repository: CommentRepositoryDep,
) -> GetCommentUseCase:
    return GetCommentUseCase(repository)


def get_create_comment_use_case(
    repository: CommentRepositoryDep,
    file_use_case: FileUseCaseDep,
) -> CreateCommentUseCase:
    return CreateCommentUseCase(repository, file_use_case)


def get_update_comment_use_case(
    repository: CommentRepositoryDep,
) -> UpdateCommentUseCase:
    return UpdateCommentUseCase(repository)


def get_delete_comment_use_case(
    repository: CommentRepositoryDep,
) -> DeleteCommentUseCase:
    return DeleteCommentUseCase(repository)


GetCommentListUseCaseDep = Annotated[
    GetCommentListUseCase,
    Depends(get_comment_list_use_case),
]

GetCommentUseCaseDep = Annotated[
    GetCommentUseCase,
    Depends(get_comment_use_case),
]

CreateCommentUseCaseDep = Annotated[
    CreateCommentUseCase,
    Depends(get_create_comment_use_case),
]

UpdateCommentUseCaseDep = Annotated[
    UpdateCommentUseCase,
    Depends(get_update_comment_use_case),
]

DeleteCommentUseCaseDep = Annotated[
    DeleteCommentUseCase,
    Depends(get_delete_comment_use_case),
]