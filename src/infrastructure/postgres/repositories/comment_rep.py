from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from ..models.comment_m import Comment
from src.domain.exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)


class CommentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[Comment]:
        try:
            s = (
                select(Comment)
                .options(selectinload(Comment.image))
                .offset(skip)
                .limit(limit)
            )
            result = await self.session.execute(s)
            return list(result.scalars().all())
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Comment",
                operation="get_list",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Comment",
                operation="get_list",
                details=str(err),
            ) from err
        
    async def get(self, Comment_id: int) -> Comment | None:
        try:
            stmt = (
                select(Comment)
                .options(selectinload(Comment.image))
                .where(Comment.id == Comment_id)
            )
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Comment",
                operation="get",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Comment",
                operation="get",
                details=str(err),
            ) from err
        
    async def create(self, comment: Comment) -> Comment:
        try:
            self.session.add(comment)
            await self.session.flush()
            await self.session.refresh(comment)
            return comment
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="create",
                obj=comment,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Comment",
                operation="create",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Comment",
                operation="create",
                details=str(err),
            ) from err

    async def update(self, comment: Comment) -> Comment:
        try:
            await self.session.flush()
            await self.session.refresh(comment)
            return comment
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="update",
                obj=comment,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Comment",
                operation="update",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Comment",
                operation="update",
                details=str(err),
            ) from err

    async def delete(self, comment: Comment) -> None:
        try:
            await self.session.delete(comment)
            await self.session.flush()
            return None
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="delete",
                obj=comment,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Comment",
                operation="delete",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Comment",
                operation="delete",
                details=str(err),
            ) from err

    def _map_integrity_error(
        self,
        *,
        err: IntegrityError,
        operation: str,
        obj: Comment,
    ) -> DatabaseError:
        message = str(err.orig).lower()

        if "foreign key" in message:
            return ForeignKeyConflictError(
                entity="Comment",
                operation=operation,
                details=str(err.orig),
            )

        if "unique" in message or "duplicate" in message:
            return DataConflictError(
                entity="Comment",
                operation=operation,
                details=str(err.orig),
            )

        return DatabaseError(
            entity="Comment",
            operation=operation,
            details=str(err.orig),
        )
