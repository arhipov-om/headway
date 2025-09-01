import random
from datetime import time

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram_dialog import DialogManager, StartMode, ShowMode

from headway.application.dto import ReminderDTO, CreateReminderDTO, UserDTO
from headway.application.services import (
    ReminderService, UserService,
)
from headway.application.value_objects import Duration
from headway.domain.entitites import Frequency
from ..callbacks import MenuCallback
from ..dialogs.start_menu import MainMenu

router = Router()


def get_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Создать напоминание", callback_data=MenuCallback(action="create_reminder").pack()),
        InlineKeyboardButton(text="Список напоминаний", callback_data=MenuCallback(action="list_reminders").pack()),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])


@router.message(Command("start"))
async def start(message: Message, dialog_manager: DialogManager):
    provider = 'telegram'
    provider_id = message.from_user.id

    user_service: UserService = dialog_manager.middleware_data.get('user_service')
    user = await user_service.get_user_by_identity(provider=provider, provider_id=message.from_user.id)
    if not user:
        user = await user_service.create_user(
            name=message.from_user.full_name,
            provider=provider,
            provider_id=str(provider_id)
        )

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
