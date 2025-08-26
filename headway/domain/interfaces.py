from typing import Protocol
from uuid import UUID

from headway.domain.entitites import User, Reminder, Motivation, Notification


class IUserRepository(Protocol):
    def create(self, user: User) -> User:
        ...

    def get(self, user_id: UUID) -> User:
        ...

    def list(self) -> list[User]:
        ...


class IReminderRepository(Protocol):
    def create(self, reminder: Reminder) -> Reminder:
        ...

    def get(self, reminder_id: UUID) -> Reminder:
        ...

    def list_by_user(self, user_id: UUID) -> list[Reminder]:
        ...

    def update(self, reminder: Reminder) -> Reminder:
        ...

    def delete(self, reminder_id: UUID) -> None:
        ...


class IMotivationRepository(Protocol):
    def list_all(self) -> list[Motivation]:
        ...

    def get_random(self) -> Motivation:
        ...


class INotificationRepository(Protocol):
    def create(self, notification: Notification) -> Notification:
        ...

    def list_pending(self) -> list[Notification]:
        ...

    def mark_sent(self, notification_id: UUID) -> None:
        ...
