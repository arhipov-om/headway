from datetime import datetime
from uuid import uuid4, UUID

from adaptix.conversion import convert, coercer

from .dto import ReminderDTO, UserDTO, CreateReminderDTO
from ..domain.entitites import Reminder, User, Frequency, Identity
from ..domain.interfaces import IUserRepository, IReminderRepository
from ..domain.value_objects import Duration, WeekDays


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def get_user_by_identity(self, provider_id: str, provider: str = 'telegram'):
        return await self.user_repo.get_by_provider(provider=provider, provider_id=provider_id)

    async def create_user(self, name: str, provider: str, provider_id: str) -> UserDTO:
        user_id = uuid4()
        identity = Identity(id=uuid4(), user_id=user_id, provider=provider, provider_id=provider_id)
        user = User(id=user_id, name=name)
        user.add_identity(identity)
        user = await self.user_repo.create(user)
        try:
            await self.user_repo.session.commit()
        except Exception as e:
            pass

        return convert(user, UserDTO)


class ReminderService:
    def __init__(self, reminder_repo: IReminderRepository):
        self.reminder_repo = reminder_repo

        self._convert_recipe = [
            coercer(str, Frequency, lambda x: Frequency(x)),
            coercer(Frequency, str, lambda x: x.value),

            coercer(str, WeekDays, lambda x: WeekDays(x)),
            coercer(WeekDays, str, lambda x: x.value),
        ]

    async def create_reminder(self, create_reminder: CreateReminderDTO) -> ReminderDTO:
        start_date = datetime.now()
        end_date = Duration(create_reminder.duration).to_delta(start_date=start_date)

        reminder = Reminder(
            id=uuid4(),
            user_id=create_reminder.user_id,
            text=create_reminder.text,
            frequency=Frequency(create_reminder.frequency),
            time=create_reminder.time,
            start_date=start_date,
            end_date=end_date,
            days=WeekDays(create_reminder.days) if create_reminder.days else WeekDays.default()
        )
        reminder = await self.reminder_repo.create(reminder)
        await self.reminder_repo.session.commit()
        return convert(reminder, ReminderDTO, recipe=self._convert_recipe)

    async def list_reminders_by_user(self, user_id: UUID) -> list[ReminderDTO]:
        reminders = await self.reminder_repo.list_by_user(user_id)
        return [convert(r, ReminderDTO, recipe=self._convert_recipe) for r in reminders]
