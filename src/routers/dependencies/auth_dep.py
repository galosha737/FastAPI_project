from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.auth.security import decode_token
from src.infrastructure.postgres.models.user_m import User
from src.use_cases.auth.login import LoginUserUseCase
from src.use_cases.auth.refresh import RefreshTokenUseCase
from src.routers.dependencies.user_dep import UserRepositoryDep

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_login_user_use_case(
    repository: UserRepositoryDep,
) -> LoginUserUseCase:
    return LoginUserUseCase(repository)


LoginUserUseCaseDep = Annotated[
    LoginUserUseCase,
    Depends(get_login_user_use_case),
]


def get_refresh_token_use_case(
    repository: UserRepositoryDep,
) -> RefreshTokenUseCase:
    return RefreshTokenUseCase(repository)


RefreshTokenUseCaseDep = Annotated[
    RefreshTokenUseCase,
    Depends(get_refresh_token_use_case),
]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    repository: UserRepositoryDep,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except ValueError as err:
        raise credentials_exception from err

    user = await repository.get(int(user_id))
    if user is None:
        raise credentials_exception

    return user


async def get_admin_user(
        current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not allowed for non-admin users"
        )
    return current_user


async def get_super_admin_user(
        current_user: Annotated[User, Depends(get_current_user)]) -> User:
    if current_user.role != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operation not allowed for non-super-admin users"
        )
    return current_user

SuperAdminDep = Annotated[User, Depends(get_super_admin_user)]