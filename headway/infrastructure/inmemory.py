from random import choice
from typing import Dict, List
from uuid import UUID

from ..domain.entitites import User, Reminder, Motivation, Notification
from ..domain.interfaces import IUserRepository, INotificationRepository, IMotivationRepository, IReminderRepository


class InMemoryDB:
    def __init__(self):
        self.users: Dict[UUID, User] = {}
        self.reminders: Dict[UUID, Reminder] = {}
        self.motivations: Dict[UUID, Motivation] = {}
        self.notifications: Dict[UUID, Notification] = {}


class UserRepository(IUserRepository):
    def __init__(self, db: InMemoryDB) -> None:
        self.db = db

    def create(self, user: User) -> User:
        self.db.users[user.id] = user
        return user

    def get(self, user_id: UUID) -> User:
        return self.db.users[user_id]

    def list(self) -> List[User]:
        return list(self.db.users.values())


class ReminderRepository(IReminderRepository):
    def __init__(self, db: InMemoryDB):
        self.db = db

    def create(self, reminder: Reminder) -> Reminder:
        self.db.reminders[reminder.id] = reminder
        return reminder

    def get(self, reminder_id: UUID) -> Reminder:
        return self.db.reminders[reminder_id]

    def list_by_user(self, user_id: UUID) -> List[Reminder]:
        return [r for r in self.db.reminders.values() if r.user_id == user_id]

    def update(self, reminder: Reminder) -> Reminder:
        self.db.reminders[reminder.id] = reminder
        return reminder

    def delete(self, reminder_id: UUID) -> None:
        self.db.reminders.pop(reminder_id, None)

    def list_all(self) -> list[Reminder]:
        return list(self.db.reminders.values())


class MotivationRepository(IMotivationRepository):
    def __init__(self, db: InMemoryDB):
        self.db = db

    def list_all(self) -> List[Motivation]:
        return list(self.db.motivations.values())

    def get_random(self) -> Motivation:
        if not self.db.motivations:
            raise ValueError("No motivations available")
        return choice(list(self.db.motivations.values()))

    def add(self, motivation: Motivation) -> Motivation:
        self.db.motivations[motivation.id] = motivation
        return motivation


class NotificationRepository(INotificationRepository):
    def __init__(self, db: InMemoryDB):
        self.db = db

    def create(self, notification: Notification) -> Notification:
        self.db.notifications[notification.id] = notification
        return notification

    def list_pending(self) -> List[Notification]:
        return [n for n in self.db.notifications.values() if not n.sent]

    def mark_sent(self, notification_id: UUID) -> None:
        if notification_id in self.db.notifications:
            self.db.notifications[notification_id].sent = True

    def list_all(self) -> list[Notification]:
        return list(self.db.notifications.values())
