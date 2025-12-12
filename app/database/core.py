import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

DATABASE_URL = str(os.environ.get("DATABASE_URL", ""))

async_engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session


def get_sync_engine(url: str):
    sync_url = url.replace("+asyncpg", "")
    return create_engine(sync_url, future=True)
