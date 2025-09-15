from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from headway.presentation.telegram.states import MainMenu, CreateReminder, ManageReminder


async def start_create_reminder(callback, button, dialog_manager: DialogManager):
    await dialog_manager.start(CreateReminder.Title)


async def back_to_main_menu(callback, button, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenu.START)


async def show_list(callback, button, dialog_manager: DialogManager):
    await dialog_manager.start(ManageReminder.List)


main_window = Window(
    Const("Главное меню:"),
    Button(
        Const("Создать напоминание"),
        id="create_reminder",
        on_click=start_create_reminder
    ),
    Button(Const("Список напоминаний"), id="reminders_list", on_click=show_list),
    state=MainMenu.START,
)

dialog = Dialog(main_window)
