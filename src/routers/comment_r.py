from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..infrastructure.postgres.database import get_db
from ..infrastructure.postgres.repositories.comment_rep import (
    CommentRepository)
from ..schems.comment_s import CommentUpdate, CommentCreate, CommentOut


router = APIRouter(prefix='/comments', tags=['Комментарий'])


def get_comment_repository(
        session: AsyncSession = Depends(get_db)
        ) -> CommentRepository:
    return CommentRepository(session)


@router.get(
    "/",
    response_model=list[CommentOut],
    status_code=status.HTTP_200_OK,
    summary="Комментарии:"
)
async def get_comments(
    skip: int = 0,
    limit: int = 10,
    repository: CommentRepository = Depends(get_comment_repository),
):
    return await repository.get_list(skip=skip, limit=limit)


@router.get(
    "/{comment_id}",
    response_model=CommentOut,
    status_code=status.HTTP_200_OK,
    summary="Комментарий:"
)
async def get_comment(
    comment_id: int,
    repository: CommentRepository = Depends(get_comment_repository),
):
    comment = await repository.get(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден!")
    return comment


@router.post(
    "/create",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать комментарий:"
)
async def create_comment(
    comment_in: CommentCreate,
    repository: CommentRepository = Depends(get_comment_repository),
):
    return await repository.create(comment_in)


@router.put(
    "/put/{comment_id}",
    response_model=CommentOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить комментарий:"
)
async def update_comment(
    comment_id: int,
    comment_in: CommentUpdate,
    repository: CommentRepository = Depends(get_comment_repository),
):
    comment = await repository.update(comment_id, comment_in)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден!")
    return comment


@router.delete(
    "/delete/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить комментарий:"
)
async def delete_comment(
    comment_id: int,
    repository: CommentRepository = Depends(get_comment_repository),
):
    comment = await repository.delete(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
