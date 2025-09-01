from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    START = State()

class CreateReminder(StatesGroup):
    Title = State()
    Frequency = State()
    Once_in_week = State()
    Frequency_week_day = State()
    Time = State()
    Duration = State()
    End = State()


class ManageReminder(StatesGroup):
    List = State()
    InnerMenu = State()