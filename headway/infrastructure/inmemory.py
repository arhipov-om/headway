from random import choice
from typing import Dict, List
from uuid import UUID

from ..domain.entitites import User, Reminder, Motivation, Notification
from ..domain.interfaces import IUserRepository, IMotivationRepository, IReminderRepository


class InMemoryDB:
    def __init__(self):
        self.users: Dict[UUID, User] = {}
        self.reminders: Dict[UUID, Reminder] = {}
        self.motivations: Dict[UUID, Motivation] = {}
        self.notifications: Dict[UUID, Notification] = {}


class UserRepository(IUserRepository):
    def __init__(self, db: InMemoryDB) -> None:
        self.db = db

    async def create(self, user: User) -> User:
        self.db.users[user.id] = user
        return user

    async def get(self, user_id: UUID) -> User:
        return self.db.users[user_id]

    async def list(self) -> List[User]:
        return list(self.db.users.values())


class ReminderRepository(IReminderRepository):
    def __init__(self, db: InMemoryDB):
        self.db = db

    async def create(self, reminder: Reminder) -> Reminder:
        self.db.reminders[reminder.id] = reminder
        return reminder

    async def get(self, reminder_id: UUID) -> Reminder:
        return self.db.reminders[reminder_id]

    async def list_by_user(self, user_id: UUID) -> List[Reminder]:
        return [r for r in self.db.reminders.values() if r.user_id == user_id]

    async def update(self, reminder: Reminder) -> Reminder:
        self.db.reminders[reminder.id] = reminder
        return reminder

    async def delete(self, reminder_id: UUID) -> None:
        self.db.reminders.pop(reminder_id, None)

    async def list_all(self) -> list[Reminder]:
        return list(self.db.reminders.values())


class MotivationRepository(IMotivationRepository):
    def __init__(self, db: InMemoryDB):
        self.db = db

    async def list_all(self) -> List[Motivation]:
        return list(self.db.motivations.values())

    async def get_random(self) -> Motivation:
        if not self.db.motivations:
            raise ValueError("No motivations available")
        return choice(list(self.db.motivations.values()))

    async def add(self, motivation: Motivation) -> Motivation:
        self.db.motivations[motivation.id] = motivation
        return motivation
