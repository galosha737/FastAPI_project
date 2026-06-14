from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.category_m import Category
from src.exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[Category]:
        try:
            s = select(Category).offset(skip).limit(limit)
            result = await self.session.execute(s)
            return list(result.scalars().all())
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Category",
                operation="get_list",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Category",
                operation="get_list",
                details=str(err),
            ) from err

    async def get(self, category_id: int) -> Category | None:
        try:
            return await self.session.get(Category, category_id)
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Category",
                operation="get",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Category",
                operation="get",
                details=str(err),
            ) from err

    async def create(self, category: Category) -> Category:
        try:
            self.session.add(category)
            await self.session.flush()
            await self.session.refresh(category)
            return category
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="create",
                obj=category,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Category",
                operation="create",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Category",
                operation="create",
                details=str(err),
            ) from err

    async def update(self, category: Category) -> Category:
        try:
            await self.session.flush()
            await self.session.refresh(category)
            return category
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="update",
                obj=category,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Category",
                operation="update",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Category",
                operation="update",
                details=str(err),
            ) from err

    async def delete(self, category: Category) -> None:
        try:
            await self.session.delete(category)
            await self.session.flush()
            return None
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="delete",
                obj=category,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Category",
                operation="delete",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Category",
                operation="delete",
                details=str(err),
            ) from err

    def _map_integrity_error(
        self,
        *,
        err: IntegrityError,
        operation: str,
        obj: Category,
    ) -> DatabaseError:
        message = str(err.orig).lower()

        if "unique" in message or "duplicate" in message:
            if "title" in message:
                return DataConflictError(
                    entity="Category",
                    operation=operation,
                    field="title",
                    value=getattr(obj, "title", None),
                    details=str(err.orig),
                )

            if "slug" in message:
                return DataConflictError(
                    entity="Category",
                    operation=operation,
                    field="slug",
                    value=getattr(obj, "slug", None),
                    details=str(err.orig),
                )

            return DataConflictError(
                entity="Category",
                operation=operation,
                details=str(err.orig),
            )

        if "foreign key" in message:
            return ForeignKeyConflictError(
                entity="Category",
                operation=operation,
                details=str(err.orig),
            )

        return DatabaseError(
            entity="Category",
            operation=operation,
            details=str(err.orig),
        )
