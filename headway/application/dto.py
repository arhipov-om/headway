from dataclasses import dataclass
from datetime import time, datetime
from uuid import UUID

from headway.application.value_objects import WeekDays, Duration
from headway.domain.entitites import Frequency


@dataclass
class UserDTO:
    id: UUID
    name: str
    timezone: str


@dataclass(kw_only=True)
class ReminderDTO:
    id: UUID
    user_id: UUID
    text: str
    frequency: Frequency
    start_day: int = None
    time: time
    start_date: datetime
    end_date: datetime
    days: WeekDays
    active: bool


@dataclass(kw_only=True)
class CreateReminderDTO:
    user_id: UUID
    text: str
    frequency: Frequency
    start_day: int = None
    duration: Duration
    time: time
    days: WeekDays = WeekDays.default()


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
