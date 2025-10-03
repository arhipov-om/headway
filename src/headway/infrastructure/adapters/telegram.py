from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from headway.application.dto import NotificationDTO
from headway.application.intefaces import IMessagingClient


class TelegramClientAdapter(IMessagingClient):
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_reminder(self, chat_id: str, notification_dto: NotificationDTO, text: str) -> Message:  # type: ignore
        return await self.bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(
                    text='Начинаю 🏳',
                    callback_data=f'start:{str(notification_dto.id)[:6]}'
                )]
            ])
        )
