from aiogram_dialog import DialogManager, ShowMode

from headway.presentation.telegram.states import ManageReminder


async def inner_reminder(_, __, dialog_manager: DialogManager, reminder_start_id, **___):
    dialog_manager.dialog_data['reminder_start_id'] = reminder_start_id
    await dialog_manager.switch_to(ManageReminder.InnerMenu, show_mode=ShowMode.EDIT)