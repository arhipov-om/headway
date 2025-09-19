import random
from types import SimpleNamespace
from uuid import UUID

from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dishka import FromDishka

from headway.application.services import UserService, MotivationService
from headway.infrastructure.send_reminder import send_reminder

router = Router()


@router.message(Command("test"))
async def process_test(message: Message, bot: Bot, command: CommandObject, user_service: FromDishka[UserService]):
    text = command.args
    if text:
        user = await user_service.get_user_by_identity(provider_id=str(message.from_user.id), provider="telegram")
        mock_reminder = SimpleNamespace(text=text,
                                        user_id=user.id)
        await send_reminder(
            bot=bot,
            reminder=mock_reminder,
        )

