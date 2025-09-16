from abc import ABC, abstractmethod
from typing import Callable, Any


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
