from dataclasses import dataclass
from datetime import datetime, time
from typing import List, Optional
from uuid import UUID


@dataclass
class User:
    id: UUID
    name: Optional[str] = None
    timezone: str = "UTC"

    def __post_init__(self):
        assert isinstance(self.id, UUID), "User.id должен быть UUID"
        if self.name is not None:
            assert self.name.strip(), "User.name не может быть пустым"


@dataclass
class Motivation:
    id: UUID
    text: str
    category: str = "affirmation"  # например: affirmation, quote

    def __post_init__(self):
        assert isinstance(self.id, UUID), "Motivation.id должен быть UUID"
        assert self.text.strip(), "Motivation.text не может быть пустым"
        assert self.category in ("affirmation", "quote"), "Неверная категория"


@dataclass
class Reminder:
    id: UUID
    user_id: UUID
    text: str  # "30 приседаний"
    frequency: str  # daily, every_2_days, weekly, custom
    custom_days: Optional[List[int]] = None  # [0,2,4] - дни недели (0=понедельник)
    time: time = time(9, 0)  # время напоминания
    duration: str = "1m"  # 1w, 2w, 1m, 3m, 6m, 12m
    active: bool = True

    VALID_FREQUENCIES = {"daily", "every_2_days", "weekly", "custom"}
    VALID_DURATIONS = {"1w", "2w", "1m", "3m", "6m", "12m"}

    def __post_init__(self):
        assert isinstance(self.id, UUID), "Reminder.id должен быть UUID"
        assert isinstance(self.user_id, UUID), "Reminder.user_id должен быть UUID"
        assert self.text.strip(), "Reminder.text не может быть пустым"
        assert self.frequency in self.VALID_FREQUENCIES, f"frequency должно быть одним из {self.VALID_FREQUENCIES}"
        if self.frequency == "custom":
            assert self.custom_days is not None and all(0 <= d <= 6 for d in self.custom_days), \
                "Для custom frequency custom_days должны быть числами 0-6"
        assert isinstance(self.time, time), "Reminder.time должен быть datetime.time"
        assert self.duration in self.VALID_DURATIONS, f"duration должно быть одним из {self.VALID_DURATIONS}"


@dataclass
class Notification:
    id: UUID
    reminder_id: UUID
    scheduled_for: datetime
    sent: bool = False
    motivation_id: Optional[UUID] = None

    def __post_init__(self):
        assert isinstance(self.id, UUID), "Notification.id должен быть UUID"
        assert isinstance(self.reminder_id, UUID), "Notification.reminder_id должен быть UUID"
        assert isinstance(self.scheduled_for, datetime), "Notification.scheduled_for должен быть datetime"
        if self.motivation_id is not None:
            assert isinstance(self.motivation_id, UUID), "Notification.motivation_id должен быть UUID"
