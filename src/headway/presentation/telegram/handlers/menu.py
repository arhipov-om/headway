import random
from datetime import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, ShowMode

from headway.application.dto import ReminderDTO, CreateReminderDTO, UserDTO
from headway.application.services import (
    ReminderService, )
from headway.domain.entitites import Frequency
from headway.domain.value_objects import Duration
from ..dialogs.start_menu import MainMenu

router = Router()


@router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenu.START, mode=StartMode.RESET_STACK, show_mode=ShowMode.EDIT)
    await message.delete()


@router.message(Command("menu"))
async def menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenu.START, mode=StartMode.RESET_STACK, show_mode=ShowMode.EDIT)
    await message.delete()


@router.message(Command('fake'))
async def create_fake(message: Message, reminder_service: ReminderService, user: UserDTO):
    texts = ["рандом", "тест", "напоминание", "дело", "штука", "фейк"]
    durations = list(Duration.VALID_DURATIONS)
    frequencies = [f.value for f in Frequency]

    def random_days() -> str:
        while True:
            s = "".join(random.choice("01") for _ in range(7))
            if "1" in s:
                return s

    for _ in range(int(message.text.split(' ')[-1])):
        reminder: ReminderDTO = await reminder_service.create_reminder(
            CreateReminderDTO(
                user_id=user.id,
                text=random.choice(texts),
                frequency=random.choice(frequencies),
                duration=random.choice(durations),
                time=time(random.randint(0, 23), random.randint(0, 59)),
                days=random_days()
            )
        )

    await message.answer('ok')
