import logging

from aiogram import Bot
from apscheduler.triggers.cron import CronTrigger
from dishka import FromDishka

from headway.application.dto import ReminderDTO
from headway.application.intefaces import IScheduler
from headway.application.services import UserService, MotivationService
from headway.infrastructure.scheduler import inject, cron

logger = logging.getLogger(__name__)

@inject
async def send_reminder(
        bot: Bot,
        reminder: ReminderDTO,
        user_service: FromDishka[UserService],
        motivation_service: FromDishka[MotivationService],
):
    user_telegram_id = await user_service.get_user_telegram_id(reminder.user_id)
    if user_telegram_id:
        text = reminder.text
        try:
            motivation = await motivation_service.get_random_motivation(task_text=text)
            text += f"\n\n"
            text += f"<i>{motivation.text}</i>"
        except Exception as e:
            logger.warning("не смог получить мотивацию %s", e)
        await bot.send_message(chat_id=user_telegram_id, text=text)


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
