from datetime import time

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

from headway.application.dto import ReminderDTO, CreateReminderDTO
from headway.application.services import ReminderService
from headway.application.value_objects import Duration
from headway.domain.entitites import Frequency
from ..callbacks import MenuCallback
from ..handlers.menu import user_mapping, get_menu_keyboard


class ReminderStates(StatesGroup):
    waiting_text = State()
    waiting_frequency = State()
    waiting_time = State()
    waiting_duration = State()


FREQUENCY_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Каждый день", callback_data="daily")],
    [InlineKeyboardButton(text="Через день", callback_data="every_2_days")],
    [InlineKeyboardButton(text="Каждую неделю", callback_data="weekly")],
])

DURATION_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1 неделя", callback_data="1w")],
    [InlineKeyboardButton(text="2 недели", callback_data="2w")],
    [InlineKeyboardButton(text="1 месяц", callback_data="1m")],
    [InlineKeyboardButton(text="3 месяца", callback_data="3m")],
    [InlineKeyboardButton(text="6 месяцев", callback_data="6m")],
    [InlineKeyboardButton(text="12 месяцев", callback_data="12m")],
])

router = Router()


# Хендлер для создания напоминания
@router.callback_query(MenuCallback.filter(F.action == "create_reminder"))
async def handle_create_reminder(callback: CallbackQuery, callback_data: MenuCallback, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите текст напоминания:")
    await state.set_state(ReminderStates.waiting_text)


@router.message(ReminderStates.waiting_text)
async def reminder_text(message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Выберите частоту:", reply_markup=FREQUENCY_KEYBOARD)
    await state.set_state(ReminderStates.waiting_frequency)


@router.callback_query(ReminderStates.waiting_frequency)
async def reminder_frequency(callback, state: FSMContext):
    await callback.answer()
    await state.update_data(frequency=callback.data)
    await callback.message.edit_text("Введите время напоминания в формате ЧЧ:ММ")
    await state.set_state(ReminderStates.waiting_time)


@router.message(ReminderStates.waiting_time)
async def reminder_time(message, state: FSMContext):
    try:
        h, m = map(int, message.text.split(":"))
    except ValueError:
        return await message.answer('абышка')
    await state.update_data(time=time(h, m))
    await message.answer("Выберите длительность:", reply_markup=DURATION_KEYBOARD)
    await state.set_state(ReminderStates.waiting_duration)


@router.callback_query(ReminderStates.waiting_duration)
async def reminder_duration(callback, state: FSMContext, reminder_service: ReminderService):
    await callback.answer()
    await state.update_data(duration=callback.data)
    data = await state.get_data()

    reminder: ReminderDTO = await reminder_service.create_reminder(
        CreateReminderDTO(
            user_id=user_mapping[callback.from_user.id],
            text=data.get('text'),
            frequency=Frequency(data.get('frequency')),
            duration=Duration(data.get('duration')),
            time=data.get('time'),
        )
    )
    await callback.message.edit_text(f"Напоминание создано: {reminder.text}\nСпасибо, записал ✅",
                                     reply_markup=get_menu_keyboard())
    await state.clear()
