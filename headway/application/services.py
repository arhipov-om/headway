from datetime import datetime
from uuid import uuid4

from adaptix.conversion import convert

from .dto import ReminderDTO, UserDTO, CreateReminderDTO
from ..domain.entitites import Reminder, User
from ..domain.interfaces import IUserRepository


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def create_user(self, name: str) -> UserDTO:
        user = User(id=uuid4(), name=name)
        user = await self.user_repo.create(user)
        return convert(user, UserDTO)


class ReminderService:
    def __init__(self, reminder_repo):
        self.reminder_repo = reminder_repo

    async def create_reminder(self, create_reminder: CreateReminderDTO) -> ReminderDTO:
        start_date = datetime.now()
        end_date = create_reminder.duration.to_delta(start_date=start_date)

        reminder = Reminder(
            id=uuid4(),
            user_id=create_reminder.user_id,
            text=create_reminder.text,
            frequency=create_reminder.frequency,
            time=create_reminder.time,
            start_date=start_date,
            end_date=end_date,
            days=create_reminder.days
        )
        reminder = await self.reminder_repo.create(reminder)
        return convert(reminder, ReminderDTO)

    async def list_reminders_by_user(self, user_id) -> list[ReminderDTO]:
        reminders = await self.reminder_repo.list_by_user(user_id)
        return [convert(r, ReminderDTO) for r in reminders]
