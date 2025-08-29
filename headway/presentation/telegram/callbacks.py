from aiogram.filters.callback_data import CallbackData

user_mapping = {}


class MenuCallback(CallbackData, prefix="menu"):
    action: str
