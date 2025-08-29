from aiogram.fsm.state import StatesGroup, State


class ReminderStates(StatesGroup):
    waiting_text = State()
    waiting_frequency = State()
    waiting_time = State()
    waiting_duration = State()
