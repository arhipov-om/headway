from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import (Button, Back, Select, Column, ScrollingGroup, Row, PrevPage, NextPage,
                                        CurrentPage)
from aiogram_dialog.widgets.text import Const, Format, Jinja

from headway.presentation.telegram.dialogs.manage_reminder import getters, actions
from headway.presentation.telegram.dialogs.start_menu import back_to_main_menu
from headway.presentation.telegram.dialogs.utils import BACK
from headway.presentation.telegram.states import ManageReminder

REMINDERS_LIST = 'reminders_list'
dialog = Dialog(
    Window(
        Const('Список напоминаний'),
        Column(
            ScrollingGroup(
                Select(
                    text=Jinja("{{item.text}} | {{item.frequency}} | {{(item.end_date - item.start_date).days}}"),
                    id="reminders_l",
                    item_id_getter=lambda x: str(x.id)[:6],
                    items='reminders',
                    on_click=actions.inner_reminder
                ),
                width=1,
                height=5,
                hide_pager=True,
                id=REMINDERS_LIST)
        ),
        Row(
            PrevPage(scroll=REMINDERS_LIST, text=Format("◀️")),
            CurrentPage(scroll=REMINDERS_LIST, text=Format("{current_page1}")),
            NextPage(scroll=REMINDERS_LIST, text=Format("▶️")),
        ),
        Button(text=BACK, on_click=back_to_main_menu, id='__back__'),
        state=ManageReminder.List,
        getter=getters.reminders_list
    ),
    Window(
        Jinja(
            "Название: {{ reminder.text }}\n"
            "Активно: {{ reminder.active }}\n"
            "Время: {{ reminder.time }}\n"
            "{% if reminder.frequency == 'custom' %}"
            "Дни: {{ reminder.days }}"
            "{% else %}"
            "Периодичность: {{ reminder.frequency }}"
            "{% endif %}"
        ),
        Back(BACK),
        state=ManageReminder.InnerMenu,
        getter=getters.get_reminder,
    )
)
