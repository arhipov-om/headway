from random import choice
from uuid import UUID

from headway.domain.entitites import User, Reminder, Motivation, Notification, Identity
from headway.domain.interfaces import IUserRepository, IMotivationRepository, IReminderRepository, IIdentityRepository


class InMemoryDB:
    def __init__(self):
        self.users: dict[UUID, User] = {}
        self.reminders: dict[UUID, Reminder] = {}
        self.motivations: dict[UUID, Motivation] = {}
        self.notifications: dict[UUID, Notification] = {}
        self.identities: dict[UUID, Identity] = {}


class UserRepository(IUserRepository):
    def __init__(self, db: InMemoryDB) -> None:
        self.db = db

    async def create(self, user: User) -> User:
        self.db.users[user.id] = user
        return user

    async def get(self, user_id: UUID) -> User:
        return self.db.users[user_id]

    async def get_by_provider(self, provider: str, provider_id: str) -> User | None:
        for k, v in self.db.users.items():
            if [i for i in v.identities if i.provider_id == provider_id and i.provider == provider]:
                return v
        return None

    async def list(self) -> list[User]:
        return list(self.db.users.values())

class IdentityRepository(IIdentityRepository):
    def __init__(self, db: InMemoryDB) -> None:
        self.db = db

    async def create(self, identity: Identity) -> Identity:
        self.db.identities[identity.id] = identity
        return identity

    async def get(self, identity_id: UUID) -> Identity:
        return self.db.identities[identity_id]


class ReminderRepository(IReminderRepository):
    def __init__(self, db: InMemoryDB):
        self.db = db

    async def create(self, reminder: Reminder) -> Reminder:
        self.db.reminders[reminder.id] = reminder
        return reminder

    async def get(self, reminder_id: UUID) -> Reminder:
        return self.db.reminders[reminder_id]

    async def list_by_user(self, user_id: UUID) -> list[Reminder]:
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

    async def list_all(self) -> list[Motivation]:
        return list(self.db.motivations.values())

    async def get_random(self) -> Motivation:
        if not self.db.motivations:
            raise ValueError("No motivations available")
        return choice(list(self.db.motivations.values()))

    async def add(self, motivation: Motivation) -> Motivation:
        self.db.motivations[motivation.id] = motivation
        return motivation
