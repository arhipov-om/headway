from dataclasses import dataclass
from datetime import time, datetime
from uuid import UUID


@dataclass
class UserDTO:
    id: UUID
    name: str
    timezone: str
    identities: list


@dataclass(kw_only=True)
class ReminderDTO:
    id: UUID
    user_id: UUID
    text: str
    frequency: str
    start_day: int = None
    time: time
    start_date: datetime
    end_date: datetime
    days: str
    active: bool


@dataclass(kw_only=True)
class CreateReminderDTO:
    user_id: UUID
    text: str
    frequency: str
    start_day: int = None
    duration: str
    time: time
    days: str


@dataclass
class MotivationDTO:
    id: UUID
    text: str
    category: str


@dataclass
class NotificationDTO:
    id: UUID
    reminder_id: UUID
    scheduled_for: datetime
    sent: bool
    motivation_text: str
