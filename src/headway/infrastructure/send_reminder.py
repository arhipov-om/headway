from aiogram import Bot
from apscheduler.triggers.cron import CronTrigger
from dishka import FromDishka

from headway.application.dto import ReminderDTO
from headway.application.intefaces import IScheduler
from headway.application.services import UserService
from headway.infrastructure.scheduler import inject, cron


@inject
async def send_reminder(bot: Bot, reminder: ReminderDTO, user_service: FromDishka[UserService]):
    user_telegram_id = await user_service.get_user_telegram_id(reminder.user_id)
    await bot.send_message(chat_id=user_telegram_id, text=reminder.text)

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
