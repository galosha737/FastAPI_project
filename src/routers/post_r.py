from fastapi import APIRouter
from starlette import status

from ..schemas.post_s import PostCreate, PostOut, PostUpdate
from .dependencies.post_dep import (
    CreatePostUseCaseDep,
    DeletePostUseCaseDep,
    GetPostListUseCaseDep,
    GetPostUseCaseDep,
    UpdatePostUseCaseDep,
)


router = APIRouter(prefix='/posts', tags=['Посты'])


@router.get(
    "/",
    response_model=list[PostOut],
    status_code=status.HTTP_200_OK,
    summary="Посты:"
)
async def get_posts(
    use_case: GetPostListUseCaseDep,
    skip: int = 0,
    limit: int = 10,
):
    return await use_case.execute(skip=skip, limit=limit)


@router.get(
    "/{post_id}",
    response_model=PostOut,
    status_code=status.HTTP_200_OK,
    summary="Пост:"
)
async def get_post(
    use_case: GetPostUseCaseDep,
    post_id: int,
):
    return await use_case.execute(post_id)


@router.post(
    "/",
    response_model=PostOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать пост:"
)
async def create_post(
    use_case: CreatePostUseCaseDep,
    post_in: PostCreate,
):
    return await use_case.execute(post_in)


@router.put(
    "/{post_id}",
    response_model=PostOut,
    status_code=status.HTTP_200_OK,
    summary="Обновить пост:"
)
async def update_post(
    use_case: UpdatePostUseCaseDep,
    post_id: int,
    post_in: PostUpdate,
):
    return await use_case.execute(post_id, post_in)


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пост:"
)
async def delete_post(
    use_case: DeletePostUseCaseDep,
    post_id: int,
):
    await use_case.execute(post_id)
