from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from ..domain.entitites import User, Notification, Motivation, Reminder


class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get(self, user_id: UUID) -> User:
        pass

    @abstractmethod
    def list(self) -> List[User]:
        pass


class IReminderRepository(ABC):
    @abstractmethod
    def create(self, reminder: Reminder) -> Reminder:
        pass

    @abstractmethod
    def get(self, reminder_id: UUID) -> Reminder:
        pass

    @abstractmethod
    def list_by_user(self, user_id: UUID) -> list[Reminder]:
        pass

    @abstractmethod
    def update(self, reminder: Reminder) -> Reminder:
        pass

    @abstractmethod
    def delete(self, reminder_id: UUID) -> None:
        pass

    @abstractmethod
    def list_all(self) -> list[Reminder]:
        pass


class IMotivationRepository(ABC):
    @abstractmethod
    def list_all(self) -> list[Motivation]:
        pass

    @abstractmethod
    def get_random(self) -> Motivation:
        pass


class INotificationRepository(ABC):
    @abstractmethod
    def create(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    def list_pending(self) -> list[Notification]:
        pass

    @abstractmethod
    def mark_sent(self, notification_id: UUID) -> None:
        pass

    @abstractmethod
    def list_all(self) -> list[Notification]:
        pass
