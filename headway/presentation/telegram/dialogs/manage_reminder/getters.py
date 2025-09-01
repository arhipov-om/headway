from aiogram.types import Update
from aiogram_dialog import DialogManager

from headway.application.dto import UserDTO, ReminderDTO
from headway.application.services import ReminderService, UserService


async def reminders_list(dialog_manager: DialogManager, event_update: Update, **_):
    user_service: UserService = dialog_manager.middleware_data.get('user_service')
    reminder_service: ReminderService = dialog_manager.middleware_data.get('reminder_service')

    user = await user_service.get_user_by_identity(provider_id=str(event_update.callback_query.from_user.id))
    data = await reminder_service.list_reminders_by_user(user_id=user.id)
    return {
        "reminders": data
    }


async def get_reminder(dialog_manager: DialogManager, event_update: Update, **_) -> dict[str, ReminderDTO] | None:
    user: UserDTO = dialog_manager.middleware_data.get('user')
    reminder_service: ReminderService = dialog_manager.middleware_data.get('reminder_service')
    reminder_start_id = dialog_manager.dialog_data.get('reminder_start_id')
    reminders = await reminder_service.list_reminders_by_user(user.id)
    for i in reminders:
        if str(i.id).startswith(reminder_start_id):
            return {
                'reminder': i
            }
