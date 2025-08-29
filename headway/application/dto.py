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


@dataclass
class ReminderDTO:
    id: UUID
    user_id: UUID
    text: str
    frequency: Frequency
    time: time
    start_date: datetime
    end_date: datetime
    days: WeekDays
    active: bool


@dataclass
class CreateReminderDTO:
    user_id: UUID
    text: str
    frequency: Frequency
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
