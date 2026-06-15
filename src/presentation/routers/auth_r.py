from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.presentation.schemas.token import Token, RefreshToken
from src.presentation.schemas.user_s import UserOut, UserCreate, ChangeUserRoleRequest
from ..dependencies.auth_dep import LoginUserUseCaseDep
from src.infrastructure.postgres.models import User
from ..dependencies.auth_dep import get_current_user, get_super_admin_user, RefreshTokenUseCaseDep
from ..dependencies.user_dep import CreateUserUseCaseDep, ChangeUserRoleUseCaseDep

router = APIRouter(prefix="/auth", tags=["Авторизация и смена роли"])


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация"
)
async def create_user(
    use_case: CreateUserUseCaseDep,
    user_in: UserCreate,
):
    return await use_case.execute(user_in)


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Вход пользователя",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    use_case: LoginUserUseCaseDep,
):
    return await use_case.execute(
        username=form_data.username,
        password=form_data.password,
    )


@router.post(
    "/refresh",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Обновление токена",
)
async def refresh_token(
    data: RefreshToken,
    use_case: RefreshTokenUseCaseDep,
):
    return await use_case.execute(
        refresh_token=data.refresh_token
    )


@router.get(
        "/users/me/",
        response_model=UserOut,
        status_code=status.HTTP_200_OK,
        summary="Текущий пользователь",
)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    return current_user


@router.patch(
    "/{user_id}/role",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Изменить роль пользователя (только суперадмин):"
)
async def change_user_role(
    use_case: ChangeUserRoleUseCaseDep,
    user_id: int,
    user_in: ChangeUserRoleRequest,
    super_admin: Annotated[User, Depends(get_super_admin_user)]
):
    return await use_case.execute(user_id, user_in, super_admin)
