class RepositoryError(Exception):
    pass


class DatabaseError(RepositoryError):
    """Общая ошибка работы с БД."""

    def __init__(
        self,
        *,
        entity: str,
        operation: str,
        details: str | None = None,
    ):
        self.entity = entity
        self.operation = operation
        self.details = details
        super().__init__(f"Database error during {operation} for {entity}")


class DataConflictError(DatabaseError):
    """Конфликт данных"""

    def __init__(
        self,
        *,
        entity: str,
        operation: str,
        field: str | None = None,
        value: str | int | None = None,
        details: str | None = None,
    ):
        self.field = field
        self.value = value
        super().__init__(
            entity=entity,
            operation=operation,
            details=details,
        )


class ForeignKeyConflictError(DatabaseError):
    """Ошибка внешнего ключа."""

    def __init__(
        self,
        *,
        entity: str,
        operation: str,
        field: str | None = None,
        value: str | int | None = None,
        details: str | None = None,
    ):
        self.field = field
        self.value = value
        super().__init__(
            entity=entity,
            operation=operation,
            details=details,
        )


class DatabaseUnavailableError(DatabaseError):
    """БД недоступна или соединение с ней оборвалось."""

    def __init__(
        self,
        *,
        entity: str,
        operation: str,
        details: str | None = None,
    ):
        super().__init__(
            entity=entity,
            operation=operation,
            details=details,
        )