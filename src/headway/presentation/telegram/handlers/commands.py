from datetime import time
from types import SimpleNamespace
from uuid import uuid4

from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dishka import FromDishka

from headway.application.dto import CreateReminderDTO
from headway.application.services import UserService, ReminderService
from headway.domain.entitites import Reminder
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
        time=time(10,10),
        days="0000000",
        ))
        await send_reminder(
            bot=bot,
            reminder=mock_reminder,
        )

