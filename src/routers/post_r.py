from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..infrastructure.postgres.database import get_db
from ..infrastructure.postgres.repositories.post_rep import PostRepository
from ..schems.post_s import PostCreate, PostOut, PostUpdate

router = APIRouter(prefix='/posts', tags=['Посты'])

# в DbSession кладем AsyncSession, которую берем из get_db
DbSession = Annotated[AsyncSession, Depends(get_db)]


def get_post_repository(session: DbSession) -> PostRepository:
    return PostRepository(session)


PostRepositoryDep = Annotated[PostRepository, Depends(get_post_repository)]


@router.get(
    "/",
    response_model=list[PostOut],
    status_code=status.HTTP_200_OK,
    summary="Посты:"
)
async def get_posts(
    repository: PostRepositoryDep,
    skip: int = 0,
    limit: int = 10,
):
    return await repository.get_list(skip=skip, limit=limit)


@router.get(
    "/{post_id}",
    response_model=PostOut,
    status_code=status.HTTP_200_OK,
    summary="Пост:"
)
async def get_post(
    repository: PostRepositoryDep,
    post_id: int,
):
    post = await repository.get(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден!")
    return post


@router.post(
    "/create",
    response_model=PostOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать пост:"
)
async def create_post(
    repository: PostRepositoryDep,
    post_in: PostCreate,
):
    return await repository.create(post_in)


@router.put(
    "/put/{post_id}",
    response_model=PostOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить пост:"
)
async def update_post(
    repository: PostRepositoryDep,
    post_id: int,
    post_in: PostUpdate,
):
    post = await repository.update(post_id, post_in)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден!")
    return post


@router.delete(
    "/delete/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пост:"
)
async def delete_post(
    repository: PostRepositoryDep,
    post_id: int,
):
    post = await repository.delete(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
