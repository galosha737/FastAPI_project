from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from src.schemas.token import Token
from src.schemas.user_s import UserOut, UserCreate
from .dependencies.auth_dep import LoginUserUseCaseDep
from infrastructure.postgres.models import User
from .dependencies.auth_dep import get_current_active_user
from .dependencies.user_dep import CreateUserUseCaseDep

router = APIRouter(prefix="/auth", tags=["Авторизация"])


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


@router.get(
        "/users/me/",
        response_model=UserOut,
        status_code=status.HTTP_200_OK,
        summary="Текущий пользователь",
)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user
