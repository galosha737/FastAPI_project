import asyncio

from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

from logging.config import fileConfig

from src.core.config import settings
from src.infrastructure.postgres.database import Base

try:
    from src.infrastructure.postgres.models.user_m import User
    from src.infrastructure.postgres.models.post_m import Post
    from src.infrastructure.postgres.models.location_m import Location
    from src.infrastructure.postgres.models.category_m import Category
    from src.infrastructure.postgres.models.comment_m import Comment
    from src.infrastructure.postgres.models.file import File
except ImportError as e:
    print(f"CRITICAL ERROR: Could not import model modules: {e}")
    raise e

CREATE_SCHEMA_QUERY = f"CREATE SCHEMA IF NOT EXISTS {settings.POSTGRES_SCHEMA};"

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

config.set_main_option("sqlalchemy.url", settings.postgres_url)

target_metadata = Base.metadata

# Временный код для проверки
print("--- DEBUG: Начало ---")
print(f"Target metadata: {target_metadata}")
print(f"Tables in metadata: {list(target_metadata.tables.keys())}")
for table_name, table_obj in target_metadata.tables.items():
    print(f"  Table '{table_name}': {table_obj.columns.keys()}")
print("--- DEBUG: Конец ---")


def filter_foreign_schemas(name, type_, parent_names):
    return type_ != "schema" or name == settings.POSTGRES_SCHEMA


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        version_table_schema=settings.POSTGRES_SCHEMA,
        include_schemas=True,
        include_name=filter_foreign_schemas,
    )

    with context.begin_transaction():
        context.execute(CREATE_SCHEMA_QUERY)
        context.run_migrations()


async def run_migrations_online(engine: AsyncEngine):
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        ),
    )

    asyncio.run(run_migrations_online(connectable))