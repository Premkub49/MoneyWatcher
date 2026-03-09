import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import pool, text
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()
sys.path.append(os.getcwd())

from app.models.base import Base  # noqa: E402

target_metadata = Base.metadata

INCLUDE_SCHEMAS = {"public", "bronze"}

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

MIGRATION_URL = os.getenv("DATABASE_URI_DIRECT", "")


def include_object(object, name, type_, reflected, compare_to):
    """Only include objects that belong to our schemas."""
    if type_ == "table":
        return object.schema in INCLUDE_SCHEMAS or object.schema is None
    return True


def do_run_migrations(connection: Connection) -> None:
    """Run migrations with bronze schema creation."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        include_object=include_object,
    )
    with context.begin_transaction():
        connection.execute(text("CREATE SCHEMA IF NOT EXISTS bronze"))
        context.run_migrations()


async def run_async_migrations() -> None:
    """Create async engine with direct connection URL and run migrations."""
    connectable = create_async_engine(
        MIGRATION_URL,
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    pass
else:
    run_migrations_online()
