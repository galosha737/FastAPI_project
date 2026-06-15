from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, OperationalError, SQLAlchemyError
from sqlalchemy.orm import selectinload

from ..models.post_m import Post
from ..models.comment_m import Comment
from src.domain.exceptions.database import (
    DataConflictError,
    DatabaseError,
    DatabaseUnavailableError,
    ForeignKeyConflictError,
)


class PostRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_list(self, skip: int = 0, limit: int = 10) -> list[Post]:
        try:
            stmt = select(Post).options(
                selectinload(Post.image),
                selectinload(Post.comments).selectinload(Comment.image)
            ).offset(skip).limit(limit)
            result = await self.session.execute(stmt)
            return list(result.scalars().all())
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Post",
                operation="get_list",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Post",
                operation="get_list",
                details=str(err),
            ) from err

    async def get(self, post_id: int) -> Post | None:
        try:
            stmt = select(Post).options(selectinload(Post.image)).where(Post.id == post_id)
            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Post",
                operation="get",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Post",
                operation="get",
                details=str(err),
            ) from err

    async def create(self, post: Post) -> Post:
        try:
            self.session.add(post)
            await self.session.flush()
            await self.session.refresh(post)
            return post
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="create",
                obj=post,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Post",
                operation="create",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Post",
                operation="create",
                details=str(err),
            ) from err

    async def update(self, post: Post) -> Post:
        try:
            await self.session.flush()
            await self.session.refresh(post)
            return post
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="update",
                obj=post,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Post",
                operation="update",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Post",
                operation="update",
                details=str(err),
            ) from err

    async def delete(self, post: Post) -> None:
        try:
            await self.session.delete(post)
            await self.session.flush()
        except IntegrityError as err:
            raise self._map_integrity_error(
                err=err,
                operation="delete",
                obj=post,
            ) from err
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Post",
                operation="delete",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Post",
                operation="delete",
                details=str(err),
            ) from err

    def _map_integrity_error(
        self,
        *,
        err: IntegrityError,
        operation: str,
        obj: Post,
    ) -> DatabaseError:
        message = str(err.orig).lower()

        if "foreign key" in message:
            return ForeignKeyConflictError(
                entity="Post",
                operation=operation,
                details=str(err.orig),
            )

        if "unique" in message or "duplicate" in message:
            return DataConflictError(
                entity="Post",
                operation=operation,
                details=str(err.orig),
            )

        return DatabaseError(
            entity="Post",
            operation=operation,
            details=str(err.orig),
        )
    
    async def get_list_for_user(self, user_id: int, skip: int = 0, limit: int = 10) -> list[Post]:
        try:
            s = (
                select(Post)
                .options(selectinload(Post.image))
                .where(
                    or_(
                        Post.author_id == user_id,
                        and_(Post.is_published, Post.author_id != user_id)
                    )
                )
                .offset(skip)
                .limit(limit)
            )
            result = await self.session.execute(s)
            return list(result.scalars().all())
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Post",
                operation="get_list_for_user",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Post",
                operation="get_list_for_user",
                details=str(err),
            ) from err

    async def get_for_user(self, post_id: int, user_id: int) -> Post | None:
        try:
            s = (
                select(Post)
                .options(selectinload(Post.image))
                .where(
                    and_(
                        Post.id == post_id,
                        or_(
                            Post.author_id == user_id,
                            Post.is_published
                        )
                    )
                )
            )
            result = await self.session.execute(s)
            return result.scalar_one_or_none()
        except OperationalError as err:
            raise DatabaseUnavailableError(
                entity="Post",
                operation="get_for_user",
                details=str(err),
            ) from err
        except SQLAlchemyError as err:
            raise DatabaseError(
                entity="Post",
                operation="get_for_user",
                details=str(err),
            ) from err
