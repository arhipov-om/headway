import logging
from typing import Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.base import BaseTrigger
from dishka import AsyncContainer
from dishka.integrations.base import wrap_injection

from headway.application.intefaces import IScheduler

logger = logging.getLogger(__name__)


class ScheduledContextHolder:
    container: AsyncContainer


def inject(func):
    async def wrapper(*args, **kwargs):
        async with ScheduledContextHolder.container() as request_dishka:
            wrapped = wrap_injection(
                func=func,
                remove_depends=True,
                container_getter=lambda _, __: request_dishka,
                is_async=True,
            )
            return await wrapped(*args, **kwargs)

    return wrapper


class AsyncScheduler(IScheduler):
    def __init__(self, container: AsyncContainer):
        ScheduledContextHolder.container = container
        self._scheduler = AsyncIOScheduler()
        self._scheduler_started = False

    async def start(self):
        if not self._scheduler_started:
            self._scheduler.start()
            self._scheduler_started = True
            logger.info("Async scheduler started")

    async def shutdown(self, wait: bool = True):
        if self._scheduler_started:
            self._scheduler.shutdown(wait=wait)
            self._scheduler_started = False
            logger.info("Async scheduler stopped")

    def add_job(
            self,
            func: Callable,
            trigger: BaseTrigger,
            *args,
            **kwargs
    ):
        self._scheduler.add_job(func, trigger, **kwargs)
        logger.info(f"Job {func.__name__} added")


def cron(days) -> str:
    day_map = {0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri', 5: 'sat', 6: 'sun'}
    active_days = [day_map[i] for i, bit in enumerate(days) if bit == '1']
    day_of_week = ','.join(active_days) if active_days else '*'
    return day_of_week
