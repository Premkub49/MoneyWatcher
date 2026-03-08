import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

Base = declarative_base()

DATABASE_URL = str(os.getenv("DATABASE_URL", ""))
async_engine = create_async_engine(DATABASE_URL, echo=False, connect_args={
    "statement_cache_size": 0
})

AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_db_session():
    """Yield an async DB session for FastAPI dependency injection."""
    async with AsyncSessionLocal() as session:
        yield session


def get_sync_engine(url: str):
    """Create a sync engine from an asyncpg URL."""
    sync_url = url.replace("+asyncpg", "")
    return create_engine(sync_url, future=True)
