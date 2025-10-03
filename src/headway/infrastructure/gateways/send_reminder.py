import logging

from aiogram import Bot
from apscheduler.triggers.cron import CronTrigger
from dishka import FromDishka

from headway.application.dto import ReminderDTO
from headway.application.intefaces import IScheduler
from headway.application.services import NotificationService
from headway.infrastructure.scheduler import inject, cron
from headway.infrastructure.adapters.telegram import TelegramClientAdapter
logger = logging.getLogger(__name__)

@inject
async def send_reminder(
        bot: Bot,
        reminder: ReminderDTO,
        notification_service: FromDishka[NotificationService],
):
    await notification_service.send(reminder_dto=reminder, message_client=TelegramClientAdapter(bot))


async def add_reminders_to_schedule(
        scheduler: IScheduler,
        reminders: list[ReminderDTO],
        bot):
    for r in reminders:
        trigger = CronTrigger(
            hour=r.time.hour,
            minute=r.time.minute,
            second=r.time.second,
            day_of_week=cron(r.days),
            start_date=r.start_date,
            end_date=r.end_date
        )
        scheduler.add_job(
            func=send_reminder,
            trigger=trigger,
            id=str(r.id),
            replace_existing=True,
            misfire_grace_time=60,
            kwargs={'reminder': r, 'bot': bot},
        )
