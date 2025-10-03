from datetime import datetime
from uuid import UUID

from adaptix._internal.conversion.facade.provider import coercer
from adaptix.conversion import ConversionRetort
from adaptix.conversion import allow_unlinked_optional
from sqlalchemy import select, and_, Update, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from headway.domain.entitites import User, Reminder, Frequency, Motivation, Notification
from headway.domain.interfaces import IUserRepository, IReminderRepository, IMotivationRepository, \
    INotificationRepository
from headway.domain.value_objects import WeekDays
from headway.infrastructure.database.sql.models import UserORM, IdentityORM, ReminderORM, NotificationORM, MotivationORM

retort = ConversionRetort(recipe=[allow_unlinked_optional()])


def int_or_none(x):
    try:
        return int(x)
    except TypeError:
        return None


reminder_retort = retort.extend(recipe=[
    allow_unlinked_optional(),
    coercer(WeekDays, str | None, lambda x: str(x.value)),
    coercer(Frequency, str, lambda x: str(x.value)),
    coercer(int | None, int, int_or_none),
    coercer(str | None, WeekDays, lambda x: WeekDays(x)),
    coercer(str, Frequency, lambda x: Frequency(x)),
])


class SQLUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: User) -> User:
        self.session.add(retort.convert(user, UserORM))
        return user

    async def get(self, user_id: UUID) -> User | None:
        result = await self.session.execute(select(UserORM).
                                            options(selectinload(UserORM.identities))
                                            .where(UserORM.id == user_id))
        orm_user = result.scalar_one_or_none()
        if not orm_user:
            return None
        return retort.convert(orm_user, User)

    async def get_by_provider(self, provider: str, provider_id: str) -> User | None:
        result = await self.session.execute(
            select(UserORM)
            .join(IdentityORM, UserORM.id == IdentityORM.user_id)
            .options(selectinload(UserORM.identities))
            .where(
                and_(
                    IdentityORM.provider_id == provider_id,
                    IdentityORM.provider == provider)
            )
        )

        orm_user = result.scalar_one_or_none()
        if not orm_user:
            return None
        return retort.convert(orm_user, User)

    async def list(self) -> list[User]:
        result = await self.session.execute(select(UserORM))
        data = result.scalars().all()
        return [retort.convert(u, User) for u in data]


# class IdentityRepository(IIdentityRepository):
#     def __init__(self, session: AsyncSession) -> None:
#         self.session = session
#
#     async def create(self, identity: Identity) -> Identity:
#
#     async def get(self, identity_id: UUID) -> Identity:
#
#
class SQLReminderRepository(IReminderRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, reminder: Reminder) -> Reminder:
        self.session.add(reminder_retort.convert(reminder, ReminderORM))
        return reminder

    async def get(self, reminder_id: UUID) -> Reminder | None:
        result = await self.session.execute(select(ReminderORM).where(ReminderORM.id == reminder_id))
        orm = result.scalar_one_or_none()
        if not orm:
            return None
        return reminder_retort.convert(orm, Reminder)

    async def list_by_user(self, user_id: UUID) -> list[Reminder]:
        result = await self.session.execute(select(ReminderORM).where(ReminderORM.user_id == user_id))
        data = result.scalars().all()
        return [reminder_retort.convert(r, Reminder) for r in data]

    async def update(self, reminder: Reminder) -> Reminder:
        pass

    async def delete(self, reminder_id: UUID) -> None:
        pass

    async def list_all(self) -> list[Reminder]:
        result = await self.session.execute(select(ReminderORM))
        data = result.scalars().all()
        return [reminder_retort.convert(r, Reminder) for r in data]


class SQLMotivationRepository(IMotivationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, motivation: Motivation) -> Motivation:
        self.session.add(retort.convert(motivation, MotivationORM))
        return motivation

    async def list_all(self) -> list[Motivation]:
        pass

    async def get_random(self) -> Motivation:
        pass

    async def add(self, motivation: Motivation) -> Motivation:
        pass


class SQLNotificationRepository(INotificationRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, notification: Notification) -> Notification:
        self.session.add(reminder_retort.convert(notification, NotificationORM))
        return notification

    async def list_pending(self) -> list[Notification]:
        pass

    async def mark_sent(self, notification_id: UUID) -> None:
        await self.session.execute(
            Update(NotificationORM).values(sent=True)
            .where(NotificationORM.id == notification_id)
        )

    async def mark_started(self, short_notification_id: str, time: datetime | None = None) -> None:
        await self.session.execute(
            Update(NotificationORM).values(started_at=time or datetime.now())
            .where(cast(NotificationORM.id, String).startswith(short_notification_id))
            # TODO: в таком случае не работают индексы
        )

    async def mark_finished(self, short_notification_id: str, time: datetime | None = None) -> None:
        await self.session.execute(
            Update(NotificationORM).values(finished_at=time or datetime.now())
            .where(cast(NotificationORM.id, String).startswith(short_notification_id))
            # TODO: в таком случае не работают индексы
        )

    async def list_all(self) -> list[Notification]:
        pass
