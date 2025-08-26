from asyncio import Protocol

from ..domain.entitites import Reminder, Notification, Motivation, User


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
