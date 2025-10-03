from datetime import time, datetime

from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from dishka import FromDishka

from headway.application.dto import CreateReminderDTO
from headway.application.services import UserService, ReminderService, NotificationService
from headway.infrastructure.gateways.send_reminder import send_reminder

router = Router()


@router.message(Command("test"))
async def process_test(message: Message, bot: Bot, command: CommandObject,
                       user_service: FromDishka[UserService],
                       reminder_service: FromDishka[ReminderService],
                       ):
    text = command.args
    if text:
        user = await user_service.get_user_by_identity(provider_id=str(message.from_user.id), provider="telegram")
        mock_reminder = await reminder_service.create_reminder(CreateReminderDTO(
            user_id=user.id,
            text=text,
            frequency="every_2_days",
            duration='1w',
            time=time(10, 10),
            days="0000000",
        ))
        await send_reminder(
            bot=bot,
            reminder=mock_reminder,
        )


@router.callback_query(F.data.startswith('start'))
async def process_start_reminder(
        callback: CallbackQuery,
        notification_service: FromDishka[NotificationService],
):
    short_notification_id = callback.data.split(':')[-1]
    now = datetime.now()
    await notification_service.mark_started(short_notification_id=short_notification_id, time=now)
    await callback.answer()
    text = callback.message.html_text
    text += f"\n\nНачато в: {now.strftime("%H:%M")}"
    await callback.message.edit_text(
        text=text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text='Готово! 🏁',
                callback_data=f'finish:{short_notification_id}'
            )]
        ])
    )

@router.callback_query(F.data.startswith('finish'))
async def process_start_reminder(
        callback: CallbackQuery,
        notification_service: FromDishka[NotificationService],
):
    short_notification_id = callback.data.split(':')[-1]
    now = datetime.now()
    await notification_service.mark_finished(short_notification_id=short_notification_id, time=now)
    await callback.answer("🎉🎉🎉")
    text = callback.message.html_text
    text += f"\nЗавершено в: {now.strftime("%H:%M")}"
    await callback.message.edit_text(text=text)
