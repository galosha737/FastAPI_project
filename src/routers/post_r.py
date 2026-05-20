from fastapi import APIRouter, HTTPException, Response
from starlette import status

from exceptions.post import PostNotFound
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
    try:
        return await use_case.execute(post_id)
    except PostNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден!",
        ) from err


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
    try:
        return await use_case.execute(post_id, post_in)
    except PostNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден!",
        ) from err


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пост:"
)
async def delete_post(
    use_case: DeletePostUseCaseDep,
    post_id: int,
):
    try:
        await use_case.execute(post_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except PostNotFound as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пост не найден!",
        ) from err
