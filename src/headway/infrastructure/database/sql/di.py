from typing import AsyncIterable

from dishka import Provider, Scope, provide, from_context
from environs import Env
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from .config import SQLConfig, get_sql_config
from .factory import create_engine, create_pool


class SQLProvider(Provider):
    scope = Scope.APP

    env = from_context(provides=Env)

    @provide
    def get_sql_config(self, env: Env) -> SQLConfig:
        return get_sql_config(env=env)

    @provide
    async def get_engine(self, db_config: SQLConfig) -> AsyncIterable[AsyncEngine]:
        engine = create_engine(db_config)
        yield engine
        await engine.dispose(True)

    @provide
    def get_pool(self, engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
        return create_pool(engine)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, pool: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with pool() as session:
            yield session
