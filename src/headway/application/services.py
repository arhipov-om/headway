import logging
from datetime import datetime
from uuid import uuid4, UUID

from adaptix.conversion import convert, coercer

from .dto import ReminderDTO, UserDTO, CreateReminderDTO, MotivationDTO, NotificationDTO
from .intefaces import IMotivationProvider
from ..domain.entitites import Reminder, User, Frequency, Identity, Notification
from ..domain.interfaces import IUserRepository, IReminderRepository, IMotivationRepository, INotificationRepository
from ..domain.value_objects import Duration, WeekDays


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    async def get_user_by_identity(self, provider_id: str, provider: str = 'telegram'):
        return await self.user_repo.get_by_provider(provider=provider, provider_id=provider_id)

    async def get_user_by_id(self, user_id: str) -> UserDTO | None:
        user = await self.user_repo.get(user_id=UUID(user_id))
        return convert(user, UserDTO)

    async def get_user_telegram_id(self, user_id: UUID) -> int | None:
        user = await self.user_repo.get(user_id=user_id)
        if not user:
            return None
        return int(user.telegram_id)

    # TODO: вынести создание User в фабричный метод.
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

    # TODO: вынести создание Reminder в фабричный метод.
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

    async def get_all_reminders(self):
        reminders = await self.reminder_repo.list_all()
        return [convert(r, ReminderDTO, recipe=self._convert_recipe) for r in reminders]


# TODO: Поменять название сервиса, так как отвечает не только за motivation.
class MotivationService:
    def __init__(
            self,
            motivation_provider: IMotivationProvider,
            motivation_repo: IMotivationRepository,
    ):
        self.motivation_provider = motivation_provider
        self.motivation_repo = motivation_repo

    async def get_random_motivation(self, task_text: str | None = None) -> MotivationDTO:
        motivation = await self.motivation_provider.get_random_motivation(task_text=task_text)
        # await self.motivation_repo.create(motivation=motivation)
        # await self.motivation_repo.session.commit()
        return convert(motivation, MotivationDTO)


class NotificationService:
    def __init__(
            self,
            notification_repo: INotificationRepository,
            reminder_service: ReminderService,
            motivation_service: MotivationService,
            user_service: UserService,
    ):
        self.notification_repo = notification_repo
        self.reminder_service = reminder_service
        self.motivation_service = motivation_service
        self.user_service = user_service

    async def create_notification(
            self,
            reminder_dto: ReminderDTO,
            motivation_id: UUID | None = None
    ) -> NotificationDTO:
        notification = Notification.create(
            reminder_id=reminder_dto.id,
            scheduled_for=reminder_dto.time,
            motivation_id=motivation_id
        )
        await self.notification_repo.create(notification)
        await self.notification_repo.session.commit()
        return convert(notification, NotificationDTO)

    async def mark_notification_sent(self, notification_id: UUID) -> bool:
        await self.notification_repo.mark_sent(notification_id=notification_id)
        await self.notification_repo.session.commit()
        return True

    async def send(self, reminder_dto: ReminderDTO, message_client) -> None:
        user_telegram_id = await self.user_service.get_user_telegram_id(reminder_dto.user_id)
        if user_telegram_id:
            text = reminder_dto.text
            try:
                motivation = await self.motivation_service.get_random_motivation(task_text=text)
                text += f"\n\n"
                text += f"<i>{motivation.text}</i>"
            except Exception as e:
                motivation = None
                logging.warning("не смог получить мотивацию %s", e.__traceback__)

            notification = await self.create_notification(
                reminder_dto=reminder_dto,
                motivation_id=motivation.id if motivation else None
            )
            await message_client.send_message(chat_id=user_telegram_id, text=text)
            await self.mark_notification_sent(notification_id=notification.id)
            await self.notification_repo.session.commit()
