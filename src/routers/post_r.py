from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from ..infrastructure.postgres.database import get_db
from ..infrastructure.postgres.repositories.post_rep import PostRepository
from ..schems.post_s import PostUpdate, PostCreate, PostOut


router = APIRouter(prefix='/posts', tags=['Посты'])


def get_post_repository(
        session: AsyncSession = Depends(get_db)
        ) -> PostRepository:
    return PostRepository(session)


@router.get(
    "/",
    response_model=list[PostOut],
    status_code=status.HTTP_200_OK,
    summary="Посты:"
)
async def get_posts(
    skip: int = 0,
    limit: int = 10,
    repository: PostRepository = Depends(get_post_repository),
):
    return await repository.get_list(skip=skip, limit=limit)


@router.get(
    "/{post_id}",
    response_model=PostOut,
    status_code=status.HTTP_200_OK,
    summary="Пост:"
)
async def get_post(
    post_id: int,
    repository: PostRepository = Depends(get_post_repository),
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
    post_in: PostCreate,
    repository: PostRepository = Depends(get_post_repository),
):
    return await repository.create(post_in)


@router.put(
    "/put/{post_id}",
    response_model=PostOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить пост:"
)
async def update_post(
    post_id: int,
    post_in: PostUpdate,
    repository: PostRepository = Depends(get_post_repository),
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
    post_id: int,
    repository: PostRepository = Depends(get_post_repository),
):
    post = await repository.delete(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Пост не найден!")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
