import operator

from aiogram import F
from aiogram_dialog import Window, Dialog, ShowMode
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Select, Column, Row, Multiselect, SwitchTo, Back, Button
from aiogram_dialog.widgets.kbd.state import Next
from aiogram_dialog.widgets.text import Const, Format

from headway.presentation.telegram.dialogs.create_reminder import actions
from headway.presentation.telegram.dialogs.create_reminder import getters
from headway.presentation.telegram.dialogs.start_menu import back_to_main_menu
from headway.presentation.telegram.dialogs.utils import BACK
from headway.presentation.telegram.states import CreateReminder

custom_week_days_window = Window(
    Format("Напоминание, {title}!"),
    Const("Выберите дни недели:"),
    Row(
        Multiselect(
            checked_text=Format("{item[name]}❤"),
            unchecked_text=Format("{item[name]}"),
            id='s_wd',
            item_id_getter=lambda item: item['id'],
            items='week_days',
            on_click=actions.store_custom_week_days
        )
    ),
    SwitchTo(
        Const('Готово'),
        id='done_wd',
        state=CreateReminder.Time,
        show_mode=ShowMode.EDIT
    ),
    SwitchTo(BACK, state=CreateReminder.Frequency, id='__back__'),
    state=CreateReminder.Frequency_week_day,
    getter=getters.get_week_days)

one_in_week_window = Window(
    Format("Напоминание, {title}!"),
    Const("Выберите день недели:"),
    Row(
        Select(
            text=Format("{item[name]}"),
            id='s_wd',
            item_id_getter=lambda item: item['id'],
            items='week_days',
            on_click=actions.store_week_days
        )
    ),
    SwitchTo(BACK, state=CreateReminder.Frequency, id='__back__'),
    state=CreateReminder.Once_in_week,
    getter=getters.get_week_days)

dialog = Dialog(
    one_in_week_window,
    custom_week_days_window,
    Window(
        Const("Введите текст напоминания:"),
        TextInput(id='title', on_success=actions.store_title),
        Button(text=BACK, on_click=back_to_main_menu, id='__back__'),
        state=CreateReminder.Title
    ),
    Window(
        Format("Напоминание, {title}!"),
        Const("Выберите частоту:"),
        Column(
            Select(
                text=Format("{item[0]}"),
                id='s_frequency',
                item_id_getter=operator.itemgetter(1),
                items="frequency",
                on_click=actions.on_freq_selected,
            )
        ),
        Back(BACK),
        state=CreateReminder.Frequency,
        getter=getters.get_data),
    Window(
        Const("Введите время напоминания в формате ЧЧ:ММ"),
        Format("Сейчас {time}", when=F["dialog_data"].get('time')),
        TextInput(id='time',
                  on_success=actions.store_time,
                  on_error=actions.not_correct_time,
                  type_factory=actions.to_time),
        Next(Const('Дальше'), when=F["dialog_data"].get('time')),
        Back(BACK),
        state=CreateReminder.Time,
        getter=getters.dialog_data
    ),
    Window(
        Const("Выберите длительность:"),
        Column(
            Select(
                Format("{item[0]}"),
                id='1',
                item_id_getter=operator.itemgetter(1),
                items="duration",
                on_click=actions.store_duration)
        ),
        Back(BACK),
        state=CreateReminder.Duration,
        getter=getters.get_duration
    )
)
