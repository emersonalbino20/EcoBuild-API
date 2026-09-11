from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from api.config import get_database_url

engine = None
AsyncSessionLocal = None


def _get_session_factory() -> async_sessionmaker[AsyncSession]:
    global engine, AsyncSessionLocal

    if AsyncSessionLocal is None:
        database_url = get_database_url()
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")

        engine = create_async_engine(database_url, pool_pre_ping=True)
        AsyncSessionLocal = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    return AsyncSessionLocal


async def get_db() -> AsyncIterator[AsyncSession]:
    session_factory = _get_session_factory()
    async with session_factory() as db:
        yield db

