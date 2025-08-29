from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from ..domain.entitites import User, Notification, Motivation, Reminder


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def get(self, user_id: UUID) -> User:
        pass

    @abstractmethod
    async def list(self) -> List[User]:
        pass


class IReminderRepository(ABC):
    @abstractmethod
    async def create(self, reminder: Reminder) -> Reminder:
        pass

    @abstractmethod
    async def get(self, reminder_id: UUID) -> Reminder:
        pass

    @abstractmethod
    async def list_by_user(self, user_id: UUID) -> list[Reminder]:
        pass

    @abstractmethod
    async def update(self, reminder: Reminder) -> Reminder:
        pass

    @abstractmethod
    async def delete(self, reminder_id: UUID) -> None:
        pass

    @abstractmethod
    async def list_all(self) -> list[Reminder]:
        pass


class IMotivationRepository(ABC):
    @abstractmethod
    async def list_all(self) -> list[Motivation]:
        pass

    @abstractmethod
    async def get_random(self) -> Motivation:
        pass


class INotificationRepository(ABC):
    @abstractmethod
    async def create(self, notification: Notification) -> Notification:
        pass

    @abstractmethod
    async def list_pending(self) -> list[Notification]:
        pass

    @abstractmethod
    async def mark_sent(self, notification_id: UUID) -> None:
        pass

    @abstractmethod
    async def list_all(self) -> list[Notification]:
        pass
