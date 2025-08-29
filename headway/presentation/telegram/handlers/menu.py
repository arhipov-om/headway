from datetime import time

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from headway.application.dto import ReminderDTO, CreateReminderDTO
from headway.application.services import (
    UserService,
    ReminderService,
)
from headway.application.value_objects import Duration
from headway.domain.entitites import Frequency
from ..callbacks import MenuCallback, user_mapping

router = Router()


def get_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Создать напоминание", callback_data=MenuCallback(action="create_reminder").pack()),
        InlineKeyboardButton(text="Список напоминаний", callback_data=MenuCallback(action="list_reminders").pack()),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])


@router.message(Command("start"))
async def start(message: Message, state: FSMContext, user_service: UserService):
    await state.clear()
    user = await user_service.create_user(message.from_user.full_name)
    user_mapping[message.from_user.id] = user.id
    await message.answer(text="Главное меню:", reply_markup=get_menu_keyboard())


@router.callback_query(MenuCallback.filter(F.action == "list_reminders"))
async def handle_list_reminders(callback: CallbackQuery, reminder_service: ReminderService):
    await callback.answer()
    user_id = callback.from_user.id
    reminders = await reminder_service.list_reminders_by_user(user_mapping[user_id])
    if reminders:
        text = "\n".join([f"{r.text} | {r.frequency.value} | {r.time}" for r in reminders])
        await callback.message.answer(text=text)
    else:
        await callback.message.answer("Список напоминаний пуст")


@router.message(Command('fake'))
async def create_fake(message: Message, reminder_service: ReminderService):
    reminder: ReminderDTO = await reminder_service.create_reminder(
        CreateReminderDTO(
            user_id=user_mapping[message.from_user.id],
            text='random',
            frequency=Frequency('daily'),
            duration=Duration('1w'),
            time=time(10, 10),
        )
    )
    await message.answer(reminder.text)
