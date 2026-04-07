from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from starlette import status
from ..infrastructure.sqlite.database import get_db
from ..repositories.comment_rep import CommentRepository
from ..schems.comment_s import CommentUpdate, CommentCreate, CommentOut


router = APIRouter(prefix='/comments', tags=['Комментарий'])

def get_comment_repository(session: Session = Depends(get_db)) -> CommentRepository:
    return CommentRepository(session)

@router.get(
    "/",
    response_model=List[CommentOut],
    status_code=status.HTTP_200_OK,
    summary="Комментарии:"
)
def get_comments(
    skip: int = 0,
    limit: int = 10,
    repository: CommentRepository = Depends(get_comment_repository),
):
    return repository.get_list(skip=skip, limit=limit)

@router.get(
    "/{comment_id}",
    response_model=CommentOut,
    status_code=status.HTTP_200_OK,
    summary="Комментарий:"
)
def get_comment(
    comment_id: int,
    repository: CommentRepository = Depends(get_comment_repository),
):
    comment = repository.get(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return comment

@router.post(
    "/create",
    response_model=CommentOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать комментарий:"
)
def create_comment(
    comment_in: CommentCreate,
    repository: CommentRepository = Depends(get_comment_repository),
):
    return repository.create(comment_in)

@router.put(
    "/put/{comment_id}",
    response_model=CommentOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить комментарий:"
)
def update_comment(
    comment_id: int,
    comment_in: CommentUpdate,
    repository: CommentRepository = Depends(get_comment_repository),
):
    comment = repository.update(comment_id, comment_in)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return comment

@router.delete(
    "/delete/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить комментарий:"
)
def delete_comment(
    comment_id: int,
    repository: CommentRepository = Depends(get_comment_repository),
):
    comment = repository.delete(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return None
