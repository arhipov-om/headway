from dataclasses import dataclass
from datetime import time
from uuid import UUID

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
    frequency: str
    time: time
    duration: str
    custom_days: list[int] | None
    active: bool

@dataclass
class MotivationDTO:
    id: UUID
    text: str
    category: str

@dataclass
class NotificationDTO:
    id: UUID
    reminder_id: UUID
    scheduled_for: str
    sent: bool
    motivation_text: str
