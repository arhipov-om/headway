from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, time
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

from headway.domain.value_objects import WeekDays


@dataclass
class User:
    id: UUID
    name: str
    timezone: str = "UTC"
    identities: list[Identity] = field(default_factory=list)

    def __post_init__(self):
        assert isinstance(self.id, UUID), "User.id должен быть UUID"
        if self.name is not None:
            assert self.name.strip(), "User.name не может быть пустым"

    def add_identity(self, identity: Identity):
        if identity not in self.identities:
            self.identities.append(identity)

    @property
    def telegram_id(self) -> str | None:
        for identity in self.identities:
            if identity.provider == 'telegram':
                return identity.provider_id
        return None


@dataclass
class Identity:
    id: UUID
    user_id: UUID
    provider_id: str
    provider: str


@dataclass
class Motivation:
    id: UUID
    text: str
    category: str = "affirmation"

    VALID_CATEGORIES = {"affirmation", "quote"}

    def __post_init__(self):
        assert isinstance(self.id, UUID), "Motivation.id должен быть UUID"
        assert self.text.strip(), "Motivation.text не может быть пустым"
        assert self.category in self.VALID_CATEGORIES, "Неверная категория"

    @classmethod
    def create(cls, text: str, category: Literal["affirmation", "quote"]) -> Motivation:
        return cls(
            id=uuid4(),
            text=text,
            category=category
        )


class Frequency(Enum):
    daily = "daily"
    every_2_days = "every_2_days"
    weekly = "weekly"
    custom = "custom"


@dataclass(kw_only=True)
class Reminder:
    id: UUID
    user_id: UUID
    text: str
    frequency: Frequency
    start_day: int = None
    days: WeekDays = WeekDays.default()
    time: time
    start_date: datetime
    end_date: datetime
    active: bool = True

    def __post_init__(self):
        if not isinstance(self.id, UUID):
            raise ValueError("Reminder.id должен быть UUID")
        if not isinstance(self.user_id, UUID):
            raise ValueError("Reminder.user_id должен быть UUID")
        if not self.text.strip():
            raise ValueError("Reminder.text не может быть пустым")
        if self.frequency == Frequency.custom and not self.days.has_active_days():
            raise ValueError("Для frequency='custom' должен быть хотя бы один активный день (1) в days")
        if not isinstance(self.time, time):
            raise ValueError("Reminder.time должен быть datetime.time")
        if not isinstance(self.start_date, datetime) or not isinstance(self.end_date, datetime):
            raise ValueError("start_date и end_date должны быть datetime")
        if self.start_date > self.end_date:
            raise ValueError("start_date не может быть позже end_date")


@dataclass
class Notification:
    id: UUID
    reminder_id: UUID
    scheduled_for: datetime
    sent: bool = False
    motivation_id: UUID | None = None

    def __post_init__(self):
        assert isinstance(self.id, UUID), "Notification.id должен быть UUID"
        assert isinstance(self.reminder_id, UUID), "Notification.reminder_id должен быть UUID"
        assert isinstance(self.scheduled_for, datetime), "Notification.scheduled_for должен быть datetime"
        if self.motivation_id is not None:
            assert isinstance(self.motivation_id, UUID), "Notification.motivation_id должен быть UUID"
