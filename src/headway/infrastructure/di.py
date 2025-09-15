from dishka import Provider, Scope, provide
from environs import Env
from sqlalchemy.ext.asyncio import AsyncSession

from headway.application.services import UserService, ReminderService
from headway.domain.interfaces import IUserRepository, IReminderRepository
from headway.infrastructure.config import get_config, Config
from headway.infrastructure.database.sql.config import SQLConfig
from headway.infrastructure.database.sql.di import SQLProvider
from headway.infrastructure.database.sql.repositories import SQLUserRepository, SQLReminderRepository


class InfrastructureProvider(Provider):
    scope = Scope.APP

    @provide
    def get_config(self, db: SQLConfig) -> Config:
        return get_config(db=db)

    @provide(scope=Scope.REQUEST)
    async def get_user_repository(self, session: AsyncSession) -> IUserRepository:
        return SQLUserRepository(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_reminder_repository(self, session: AsyncSession) -> IReminderRepository:
        return SQLReminderRepository(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_user_service(self, user_repository: IUserRepository) -> UserService:
        return UserService(user_repo=user_repository)

    @provide(scope=Scope.REQUEST)
    async def get_reminder_service(self, reminder_repo: IReminderRepository) -> ReminderService:
        return ReminderService(reminder_repo=reminder_repo)

def get_providers():
    return [
        SQLProvider(),
        InfrastructureProvider(),
    ]