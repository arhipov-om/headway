from abc import ABC, abstractmethod
from typing import Callable, Any

from headway.application.dto import NotificationDTO
from headway.domain.entitites import Motivation


class IScheduler(ABC):
    @abstractmethod
    async def start(self):
        ...

    @abstractmethod
    async def shutdown(self):
        ...

    @abstractmethod
    def add_job(self, func: Callable, trigger: Any, *args, **kwargs):
        ...


# TODO: возможно это должно быть в слое Domain.
class IMotivationProvider(ABC):
    @abstractmethod
    async def get_random_motivation(self, task_text: str | None = None) -> Motivation:
        ...

class IMessagingClient(ABC):
    @abstractmethod
    async def send_reminder(self, chat_id: str, notification_dto: NotificationDTO, text: str) -> Any:
        """Send a message to the specified chat ID."""
        pass