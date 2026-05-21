from fastapi import APIRouter
from starlette import status

from .dependencies.comment_dep import (
    CreateCommentUseCaseDep,
    DeleteCommentUseCaseDep,
    GetCommentListUseCaseDep,
    GetCommentUseCaseDep,
    UpdateCommentUseCaseDep,
)
from ..schemas.comment_s import CommentCreate, CommentOut, CommentUpdate


router = APIRouter(prefix='/comments', tags=['Комментарии'])


@router.get(
    "/",
    response_model=list[CommentOut],
    status_code=status.HTTP_200_OK,
    summary="Комментарии:"
)
async def get_comments(
    use_case: GetCommentListUseCaseDep,
    skip: int = 0,
    limit: int = 10,
):
    return await use_case.execute(skip=skip, limit=limit)


@router.get(
    "/{comment_id}",
    response_model=CommentOut,
    status_code=status.HTTP_200_OK,
    summary="Комментарий:"
)
async def get_comment(
    use_case: GetCommentUseCaseDep,
    comment_id: int,
):
    return await use_case.execute(comment_id)


@router.post(
    "/",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать комментарий:"
)
async def create_comment(
    use_case: CreateCommentUseCaseDep,
    comment_in: CommentCreate,
):
    return await use_case.execute(comment_in)


@router.put(
    "/{comment_id}",
    response_model=CommentOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить комментарий:"
)
async def update_comment(
    use_case: UpdateCommentUseCaseDep,
    comment_id: int,
    comment_in: CommentUpdate,
):
    return await use_case.execute(comment_id, comment_in)



@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить комментарий:"
)
async def delete_comment(
    use_case: DeleteCommentUseCaseDep,
    comment_id: int,
):
    await use_case.execute(comment_id)
