from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, File, Form
from starlette import status

from src.infrastructure.postgres.models.user_m import User
from .dependencies.auth_dep import get_current_user
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
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = 0,
    limit: int = 10,
):
    return await use_case.execute(skip=skip, limit=limit, current_user=current_user)


@router.get(
    "/{post_id}",
    response_model=PostOut,
    status_code=status.HTTP_200_OK,
    summary="Пост:"
)
async def get_post(
    use_case: GetPostUseCaseDep,
    current_user: Annotated[User, Depends(get_current_user)],
    post_id: int,
):
    return await use_case.execute(post_id, current_user=current_user)


@router.post(
    "/",
    response_model=PostOut,
    status_code=status.HTTP_201_CREATED,
    summary="Создать пост:"
)
async def create_post(
    current_user: Annotated[User, Depends(get_current_user)],
    use_case: CreatePostUseCaseDep,
    title: str = Form(...),
    text: str = Form(...),
    is_published: bool = Form(False),
    category_id: int | None = Form(None),
    location_id: int | None = Form(None),
    image: UploadFile | None = File(None),
):
    post_in = PostCreate(
        title=title,
        text=text,
        is_published=is_published,
        category_id=category_id,
        location_id=location_id
    )
    return await use_case.execute(post_in, image, current_user)


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
    current_user: Annotated[User, Depends(get_current_user)],
):
    return await use_case.execute(post_id, post_in, current_user)


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пост:"
)
async def delete_post(
    use_case: DeletePostUseCaseDep,
    post_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
):
    await use_case.execute(post_id, current_user)
