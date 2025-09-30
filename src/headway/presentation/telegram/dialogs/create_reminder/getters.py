from aiogram_dialog import DialogManager


async def get_data(dialog_manager: DialogManager, **_):
    frequency = [
        ('Каждый день', 'daily'),
        ('Через день', 'every_other_day'),
        ('Каждые два дня', 'every_2_days'),
        ('Раз в неделю', 'weekly'),
        ('Указать вручную', 'custom'),
    ]
    return {
        'frequency': frequency,
        'title': dialog_manager.find("title").get_value()
    }

async def dialog_data(**_):
    return _['dialog_manager'].dialog_data

async def get_week_days(dialog_manager: DialogManager, **_):
    days = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    week_days = [{"name": v, "id": i} for i, v in enumerate(days)]
    return {
        'week_days': week_days,
        'title': dialog_manager.find("title").get_value()
    }


async def get_duration(dialog_manager: DialogManager, **_):
    duration = [("1 неделя", "1w"),
                ("2 недели", "2w"),
                ("1 месяц", "1m"),
                ("3 месяца", "3m"),
                ("6 месяцев", "6m"),
                ("12 месяцев", "12m")]
    return {
        'duration': duration,
    }
