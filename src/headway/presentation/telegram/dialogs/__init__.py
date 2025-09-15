from .create_reminder.dialogs import dialog as create_reminder
from .manage_reminder.dialogs import dialog as manage_reminder
from .start_menu import dialog as start_menu

# all_dialogs = Dialog()
# all_dialogs.include_routers(
# )

# __all__ = ["all_dialogs"]
__all__ = [
    "start_menu",
    "create_reminder",
    "manage_reminder"
]
