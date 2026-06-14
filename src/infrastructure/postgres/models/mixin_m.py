from datetime import datetime, timezone

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column


def time_now():
    return datetime.now(timezone.utc)


class PubAndCreate:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=time_now,
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=time_now,
        onupdate=time_now,
        nullable=False
    )
