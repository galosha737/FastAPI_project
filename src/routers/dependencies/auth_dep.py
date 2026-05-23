from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from auth.security import decode_access_token
from infrastructure.postgres.models import User
from use_cases.auth.login import LoginUserUseCase
from .user_dep import UserRepositoryDep


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_login_user_use_case(
    repository: UserRepositoryDep,
) -> LoginUserUseCase:
    return LoginUserUseCase(repository)


LoginUserUseCaseDep = Annotated[
    LoginUserUseCase,
    Depends(get_login_user_use_case),
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
        payload = decode_access_token(token)
        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except ValueError as err:
        raise credentials_exception from err

    user = await repository.get(int(user_id))
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user
