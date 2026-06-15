from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError

from ..models.user_m import User
from src.domain.exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[User]:
        try:
            s = select(User).offset(skip).limit(limit)
            result = await self.session.execute(s)
            return list(result.scalars().all())
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="User",
                operation="get_list",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="User",
                operation="get_list",
                details=str(err),
            ) from err

    async def get(self, user_id: int) -> User | None:
        try:
            return await self.session.get(User, user_id)
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="User",
                operation="get",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="User",
                operation="get",
                details=str(err),
            ) from err
        
    async def get_by_username(self, username: str) -> User | None:
        try:
            s = select(User).where(User.username == username)
            result = await self.session.execute(s)
            return result.scalar_one_or_none()
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="User",
                operation="get",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="User",
                operation="get",
                details=str(err),
            ) from err

    async def create(self, user: User) -> User:
        try:
            self.session.add(user)
            await self.session.flush()
            await self.session.refresh(user)
            return user
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="create",
                obj=user,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="User",
                operation="create",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="User",
                operation="create",
                details=str(err),
            ) from err

    async def update(self, user: User) -> User:
        try:
            await self.session.flush()
            await self.session.refresh(user)
            return user
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="update",
                obj=user,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="User",
                operation="update",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="User",
                operation="update",
                details=str(err),
            ) from err

    async def delete(self, user: User) -> None:
        try:
            await self.session.delete(user)
            await self.session.flush()
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="delete",
                obj=user,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="User",
                operation="delete",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="User",
                operation="delete",
                details=str(err),
            ) from err

    def _map_integrity_error(
        self,
        *,
        err: IntegrityError,
        operation: str,
        obj: User,
    ) -> DatabaseError:
        message = str(err.orig).lower()

        if "unique" in message or "duplicate" in message:
            if "username" in message:
                return DataConflictError(
                    entity="User",
                    operation=operation,
                    field="username",
                    value=getattr(obj, "username", None),
                    details=str(err.orig),
                )

            if "email" in message:
                return DataConflictError(
                    entity="User",
                    operation=operation,
                    field="email",
                    value=getattr(obj, "email", None),
                    details=str(err.orig),
                )

            return DataConflictError(
                entity="User",
                operation=operation,
                details=str(err.orig),
            )

        if "foreign key" in message:
            return ForeignKeyConflictError(
                entity="User",
                operation=operation,
                details=str(err.orig),
            )

        return DatabaseError(
            entity="User",
            operation=operation,
            details=str(err.orig),
        )