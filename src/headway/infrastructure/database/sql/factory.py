from typing import AsyncIterable

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession, AsyncEngine

from headway.infrastructure.database.sql.config import SQLConfig


def create_engine(config: SQLConfig) -> AsyncEngine:
    engine = create_async_engine(
        url=config.url_with_driver,
        echo=config.DB_ECHO,
        pool_size=config.DB_POOL_SIZE,
    )
    return engine


def create_pool(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    pool = async_sessionmaker(engine, expire_on_commit=False)
    return pool


async def get_session(pool: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
    async with pool() as session:
        yield session
