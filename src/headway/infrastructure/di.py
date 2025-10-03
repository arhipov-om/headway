from dishka import Provider, Scope, provide, AsyncContainer
from environs import Env
from sqlalchemy.ext.asyncio import AsyncSession

from headway.application.intefaces import IScheduler, IMotivationProvider
from headway.application.services import UserService, ReminderService, MotivationService, NotificationService
from headway.domain.interfaces import IUserRepository, IReminderRepository, IMotivationRepository, \
    INotificationRepository
from headway.infrastructure.config import get_config, Config, AIConfig, get_ai_config
from headway.infrastructure.database.sql.config import SQLConfig
from headway.infrastructure.database.sql.di import SQLProvider
from headway.infrastructure.database.sql.repositories import SQLUserRepository, SQLReminderRepository, \
    SQLMotivationRepository, SQLNotificationRepository
from headway.infrastructure.gateways.motivation import MotivationProvider
from headway.infrastructure.scheduler import AsyncScheduler


class InfrastructureProvider(Provider):
    scope = Scope.APP

    @provide
    def get_ai_config(self, env: Env) -> AIConfig:
        return get_ai_config(env=env)

    @provide
    def get_config(self, db: SQLConfig, ai: AIConfig) -> Config:
        return get_config(db=db, ai=ai)

    @provide(scope=Scope.REQUEST)
    async def get_user_repository(self, session: AsyncSession) -> IUserRepository:
        return SQLUserRepository(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_reminder_repository(self, session: AsyncSession) -> IReminderRepository:
        return SQLReminderRepository(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_motivation_repository(self, session: AsyncSession) -> IMotivationRepository:
        return SQLMotivationRepository(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_notification_repository(self, session: AsyncSession) -> INotificationRepository:
        return SQLNotificationRepository(session=session)

    @provide(scope=Scope.REQUEST)
    async def get_user_service(self, user_repository: IUserRepository) -> UserService:
        return UserService(user_repo=user_repository)

    @provide(scope=Scope.REQUEST)
    async def get_reminder_service(self, reminder_repo: IReminderRepository) -> ReminderService:
        return ReminderService(reminder_repo=reminder_repo)

    @provide(scope=Scope.REQUEST)
    async def get_motivation_service(
            self,
            motivation_repo: IMotivationRepository,
            motivation_provider: IMotivationProvider,
    ) -> MotivationService:
        return MotivationService(
            motivation_repo=motivation_repo,
            motivation_provider=motivation_provider,
        )

    @provide(scope=Scope.REQUEST)
    async def get_notification_service(
            self,
            notification_repo: INotificationRepository,
            reminder_service: ReminderService,
            motivation_service: MotivationService,
            user_service: UserService,
    ) -> NotificationService:
        return NotificationService(
            notification_repo=notification_repo,
            reminder_service=reminder_service,
            motivation_service=motivation_service,
            user_service=user_service,
        )

    @provide(scope=Scope.APP)
    async def get_scheduler(self, container: AsyncContainer) -> IScheduler:
        return AsyncScheduler(container=container)

    @provide(scope=Scope.REQUEST)
    async def get_motivation_provider(self, ai_config: AIConfig) -> IMotivationProvider:
        return MotivationProvider(config=ai_config)


def get_providers():
    return [
        SQLProvider(),
        InfrastructureProvider(),
    ]
