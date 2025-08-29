from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta


@dataclass(frozen=True)
class WeekDays:
    value: str

    def __post_init__(self):
        # Проверка типа
        if not isinstance(self.value, str):
            raise ValueError("Days.value должен быть строкой")

        # Проверка длины
        if len(self.value) != 7:
            raise ValueError("Days.value должен содержать ровно 7 символов")

        # Проверка допустимых символов
        if not all(c in "01" for c in self.value):
            raise ValueError("Days.value должен содержать только '0' или '1'")

    def is_active(self, weekday: int) -> bool:
        """Проверяет, активен ли указанный день недели (0=понедельник, 6=воскресенье)."""
        if not 0 <= weekday <= 6:
            raise ValueError("weekday должен быть от 0 до 6")
        return self.value[weekday] == "1"

    def has_active_days(self) -> bool:
        """Проверяет, есть ли хотя бы один активный день."""
        return "1" in self.value

    @classmethod
    def default(cls) -> WeekDays:
        """Возвращает значение по умолчанию: '0000000'."""
        return cls(value="0000000")


@dataclass(frozen=True)
class Duration:
    value: str

    VALID_DURATIONS = {"1w", "2w", "1m", "3m", "6m", "12m"}

    def __post_init__(self):
        if self.value not in self.VALID_DURATIONS:
            raise ValueError(f"Duration.value должно быть одним из {self.VALID_DURATIONS}")

    def to_delta(self, start_date: datetime) -> datetime:
        """Конвертирует в end_date, учитывая календарные дни."""
        if self.value.endswith("w"):
            weeks = int(self.value[:-1])
            return start_date + timedelta(weeks=weeks)
        else:
            months = int(self.value[:-1])
            return start_date + relativedelta(months=months)
