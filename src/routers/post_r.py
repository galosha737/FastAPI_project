from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from starlette import status
from src.infrastructure.sqlite.database import get_db
from src.repositories.post_rep import PostRepository
from src.schems.post_s import PostUpdate, PostCreate, PostOut


router = APIRouter(prefix='/posts', tags=['Пост'])

def get_post_repository(session: Session = Depends(get_db)) -> PostRepository:
    return PostRepository(session)

@router.get(
    "/",
    response_model=List[PostOut],
    status_code=status.HTTP_200_OK,
    summary="Посты:"
)
def get_posts(
    skip: int = 0,
    limit: int = 10,
    repository: PostRepository = Depends(get_post_repository),
):
    return repository.get_list(skip=skip, limit=limit)

@router.get(
    "/{post_id}",
    response_model=PostOut,
    status_code=status.HTTP_200_OK,
    summary="Пост:"
)
def get_post(
    post_id: int,
    repository: PostRepository = Depends(get_post_repository),
):
    post = repository.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post

@router.post(
    "/create",
    response_model=PostOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать Пост:"
)
def create_post(
    post_in: PostCreate,
    repository: PostRepository = Depends(get_post_repository),
):
    return repository.create(post_in)

@router.put(
    "/put/{post_id}",
    response_model=PostOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить пост:"
)
def update_post(
    post_id: int,
    post_in: PostUpdate,
    repository: PostRepository = Depends(get_post_repository),
):
    post = repository.update(post_id, post_in)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return post

@router.delete(
    "/delete/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пост:"
)
def delete_post(
    post_id: int,
    repository: PostRepository = Depends(get_post_repository),
):
    post = repository.delete(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден")
    return None
