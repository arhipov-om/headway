from aiogram.types import Update
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from headway.application.dto import UserDTO, ReminderDTO
from headway.application.services import ReminderService, UserService

@inject
async def reminders_list(
        dialog_manager: DialogManager,
        event_update: Update,
        user_service: FromDishka[UserService],
        reminder_service: FromDishka[ReminderService],
        **_):
    if not dialog_manager.dialog_data.get('reminders'):
        user = await user_service.get_user_by_identity(provider_id=str(event_update.callback_query.from_user.id))
        data = await reminder_service.list_reminders_by_user(user_id=user.id)
        dialog_manager.dialog_data['reminders'] = data
    else:
        data = dialog_manager.dialog_data.get('reminders')
    return {"reminders": data}


@inject
async def get_reminder(
        dialog_manager: DialogManager,
        event_update: Update,
        reminder_service: FromDishka[ReminderService],
        **_) -> dict[str, ReminderDTO] | None:
    user: UserDTO = dialog_manager.middleware_data.get('user')
    reminder_start_id = dialog_manager.dialog_data.get('reminder_start_id')
    reminders = await reminder_service.list_reminders_by_user(user.id)
    for i in reminders:
        if str(i.id).startswith(reminder_start_id):
            return {
                'reminder': i
            }
