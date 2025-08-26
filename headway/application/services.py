from asyncio import Protocol
from datetime import datetime
from uuid import uuid4

from .dto import ReminderDTO, NotificationDTO, UserDTO
from ..domain.entitites import Reminder, Notification, Motivation, User
from ..domain.interfaces import IUserRepository, INotificationRepository, IReminderRepository, IMotivationRepository


class IReminderScheduler(Protocol):
    """Генерация Notification для Reminder на основании frequency, duration, custom_days"""

    def schedule(self, reminder: Reminder) -> list[Notification]:
        ...


class IMotivationGenerator(Protocol):
    """Выбор мотивационной цитаты для уведомления"""

    def generate(self) -> Motivation:
        ...


class INotificationSender(Protocol):
    """Отправка уведомления пользователю (например, через push или бот)"""

    def send(self, notification: Notification, user: User, motivation: Motivation) -> None:
        ...


class UserService:
    def __init__(self, user_repo: IUserRepository):
        self.user_repo = user_repo

    def create_user(self, name: str) -> UserDTO:
        user = User(id=uuid4(), name=name)
        user = self.user_repo.create(user)
        return UserDTO(**user.__dict__)


class ReminderService:
    def __init__(self, reminder_repo):
        self.reminder_repo = reminder_repo

    def create_reminder(self, user_id, text, frequency, time, duration, custom_days=None) -> ReminderDTO:
        reminder = Reminder(
            id=uuid4(),
            user_id=user_id,
            text=text,
            frequency=frequency,
            time=time,
            duration=duration,
            custom_days=custom_days
        )
        reminder = self.reminder_repo.create(reminder)
        return ReminderDTO(**reminder.__dict__)

    def list_reminders_by_user(self, user_id) -> list[ReminderDTO]:
        reminders = self.reminder_repo.list_by_user(user_id)
        return [ReminderDTO(**r.__dict__) for r in reminders]


class NotificationService:
    def __init__(self,
                 notification_repo: INotificationRepository,
                 reminder_repo: IReminderRepository,
                 motivation_repo: IMotivationRepository):
        self.notification_repo = notification_repo
        self.reminder_repo = reminder_repo
        self.motivation_repo = motivation_repo

    def generate_notifications(self) -> list[NotificationDTO]:
        result = []
        for reminder in self.reminder_repo.list_all():
            # motivation = self.motivation_repo.get_random()
            motivation = Motivation(id=uuid4(), text='пока нет, но скоро будут')
            notification = Notification(
                id=uuid4(),
                reminder_id=reminder.id,
                scheduled_for=datetime.now(),
                motivation_id=motivation.id
            )
            self.notification_repo.create(notification)
            dto = NotificationDTO(
                id=notification.id,
                reminder_id=reminder.id,
                scheduled_for=str(notification.scheduled_for),
                sent=notification.sent,
                motivation_text=motivation.text
            )
            result.append(dto)
        return result

    def list_notifications(self):
        return self.notification_repo.list_all()