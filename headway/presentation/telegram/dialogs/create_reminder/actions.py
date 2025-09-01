import re
from datetime import time
from uuid import uuid4

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog import ShowMode

from headway.application.dto import CreateReminderDTO, UserDTO
from headway.application.services import ReminderService
from headway.presentation.telegram.states import CreateReminder


async def store_title(message: Message, __, dialog_manager: DialogManager, title: str, **___):
    await message.delete()
    dialog_manager.dialog_data['title'] = title
    await dialog_manager.next(show_mode=ShowMode.EDIT)


async def store_time(_, __, dialog_manager: DialogManager, time_data: time, **___):
    dialog_manager.dialog_data['time'] = time_data
    await dialog_manager.next()


def to_time(user_input: str) -> time:
    pattern = r'\b([01]?\d|2[0-3])[:\s]([0-5]\d)\b'
    match = re.search(pattern, user_input)
    if match:
        h, m = map(int, match.groups())
        return time(hour=h, minute=m)
    raise ValueError


async def not_correct_time(m: Message, *_):
    await m.answer("Попробуй HH:MM (10:30)")


async def on_freq_selected(_, __, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data['frequency'] = item_id
    if item_id == 'weekly':
        return await dialog_manager.switch_to(CreateReminder.Once_in_week)
    elif item_id == 'custom':
        return await dialog_manager.switch_to(CreateReminder.Frequency_week_day)
    await dialog_manager.switch_to(CreateReminder.Time)
    return None


def toggle_bit(old_days: str, index: int):
    binary_list = list(map(int, str(old_days)))
    binary_list[index] = 1 - binary_list[index]
    new_days = ''.join(map(str, binary_list))
    return new_days


async def store_custom_week_days(_, __, dialog_manager: DialogManager, week_days_index, **___):
    dialog_manager.dialog_data['week_days'] = toggle_bit(
        old_days=dialog_manager.dialog_data.get('week_days', '0000000'),
        index=int(week_days_index)
    )


async def store_week_days(_, __, dialog_manager: DialogManager, week_days, **___):
    dialog_manager.dialog_data['week_days'] = ''
    await dialog_manager.switch_to(CreateReminder.Time)


async def store_duration(callback: CallbackQuery, __, dialog_manager: DialogManager, duration: time, **___):
    dialog_manager.dialog_data['duration'] = duration

    reminder_service: ReminderService = dialog_manager.middleware_data.get('reminder_service')
    user: UserDTO = dialog_manager.middleware_data.get('user')
    await reminder_service.create_reminder(
        create_reminder=CreateReminderDTO
            (
            user_id=user.id,
            text=dialog_manager.dialog_data.get('title'),
            frequency=dialog_manager.dialog_data.get('frequency'),
            # start_day=dialog_manager.dialog_data.get('week_days'),
            duration=dialog_manager.dialog_data.get('duration'),
            time=dialog_manager.dialog_data.get('time'),
            days=dialog_manager.dialog_data.get('week_days'),
        )
    )

    # TODO: тут отправить в сервис
    # await dialog_manager.next()  # End
