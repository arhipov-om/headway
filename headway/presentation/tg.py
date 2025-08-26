import asyncio
from datetime import time
from uuid import uuid4

from aiogram import Bot, Dispatcher, F, BaseMiddleware
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

# DTO и сервисы
from headway.application.dto import ReminderDTO, UserDTO
from headway.application.services import UserService, ReminderService, NotificationService
from headway.infrastructure.inmemory import UserRepository, InMemoryDB, ReminderRepository, NotificationRepository, \
    MotivationRepository


# ---------------------
# FSM состояния
# ---------------------
class ReminderStates(StatesGroup):
    waiting_text = State()
    waiting_frequency = State()
    waiting_time = State()
    waiting_duration = State()


# ---------------------
# Inline клавиатуры
# ---------------------
MAIN_MENU = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Создать напоминание", callback_data="menu_create_reminder")],
    [InlineKeyboardButton(text="Список напоминаний", callback_data="menu_list_reminders")],
    [InlineKeyboardButton(text="Генерация уведомлений", callback_data="menu_generate_notifications")],
    [InlineKeyboardButton(text="Список уведомлений", callback_data="menu_list_notifications")],
])

FREQUENCY_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Каждый день", callback_data="daily")],
    [InlineKeyboardButton(text="Через день", callback_data="every_2_days")],
    [InlineKeyboardButton(text="Каждую неделю", callback_data="weekly")],
])

DURATION_KEYBOARD = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="1 неделя", callback_data="1w")],
    [InlineKeyboardButton(text="2 недели", callback_data="2w")],
    [InlineKeyboardButton(text="1 месяц", callback_data="1m")],
    [InlineKeyboardButton(text="3 месяца", callback_data="3m")],
    [InlineKeyboardButton(text="6 месяцев", callback_data="6m")],
    [InlineKeyboardButton(text="12 месяцев", callback_data="12m")],
])

router = Router()

user_mapping = {}


@router.message(Command("start"))
async def start(message: Message, state: FSMContext, user_service: UserService):
    await state.clear()
    user = user_service.create_user(message.from_user.full_name)
    user_mapping[message.from_user.id] = user.id
    await message.answer(text="Главное меню:", reply_markup=MAIN_MENU)


@router.callback_query(F.data.startswith("menu_"))
async def menu_handler(callback: CallbackQuery, state: FSMContext, reminder_service: ReminderService,
                       notification_service: NotificationService):
    await callback.answer()
    action = callback.data

    if action == "menu_create_reminder":
        await callback.message.answer("Введите текст напоминания:")
        await state.set_state(ReminderStates.waiting_text)
    elif action == "menu_list_reminders":
        reminders = reminder_service.list_reminders_by_user(user_mapping[callback.from_user.id])
        if reminders:
            for r in reminders:
                await callback.message.answer(f"{r.id} | {r.text} | {r.frequency} | {r.time}")
        else:
            await callback.message.answer("Список напоминаний пуст")
    elif action == "menu_generate_notifications":
        notifications = notification_service.generate_notifications()
        await callback.message.answer(f"Создано {len(notifications)} уведомлений")
    elif action == "menu_list_notifications":
        notifications = notification_service.list_notifications()
        if notifications:
            for n in notifications:
                await callback.message.answer(f"Напоминание: {n.reminder_id} | Мотивация: {n.motivation_text}")
        else:
            await callback.message.answer("Список уведомлений пуст")

# ---------------------
# Шаги создания напоминания
# ---------------------
@router.message(ReminderStates.waiting_text)
async def reminder_text(message, state: FSMContext):
    await state.update_data(text=message.text)
    await message.answer("Выберите частоту:", reply_markup=FREQUENCY_KEYBOARD)
    await state.set_state(ReminderStates.waiting_frequency)


@router.callback_query(ReminderStates.waiting_frequency)
async def reminder_frequency(callback, state: FSMContext):
    await callback.answer()
    await state.update_data(frequency=callback.data)
    await callback.message.edit_text("Введите время напоминания в формате ЧЧ:ММ")
    await state.set_state(ReminderStates.waiting_time)


@router.message(ReminderStates.waiting_time)
async def reminder_time(message, state: FSMContext):
    h, m = map(int, message.text.split(":"))
    await state.update_data(time=time(h, m))
    await message.answer("Выберите длительность:", reply_markup=DURATION_KEYBOARD)
    await state.set_state(ReminderStates.waiting_duration)


@router.callback_query(ReminderStates.waiting_duration)
async def reminder_duration(callback, state: FSMContext, reminder_service: ReminderService,
                            notification_service: NotificationService):
    await callback.answer()
    await state.update_data(duration=callback.data)
    data = await state.get_data()

    reminder: ReminderDTO = reminder_service.create_reminder(
        user_id=user_mapping[callback.from_user.id],
        text=data["text"],
        frequency=data["frequency"],
        time=data["time"],
        duration=data["duration"]
    )
    notification_service.generate_notifications()

    await callback.message.edit_text(f"Напоминание создано: {reminder.text}\nСпасибо, записал ✅",
                                     reply_markup=MAIN_MENU)
    await state.clear()


class InjectMiddleware(BaseMiddleware):
    def __init__(self, data) -> None:
        self.data = data

    async def __call__(self, handler, event, data):
        for k, v in self.data.items():
            data[k] = v
        return await handler(event, data)


# ---------------------
# Запуск
# ---------------------
async def main():
    db = InMemoryDB()

    user_repo = UserRepository(db)
    reminder_repo = ReminderRepository(db)
    notification_repo = NotificationRepository(db)
    motivation_repo = MotivationRepository(db)

    user_service = UserService(user_repo=user_repo)

    reminder_service = ReminderService(reminder_repo=reminder_repo)
    notification_service = NotificationService(
        reminder_repo=reminder_repo,
        notification_repo=notification_repo,
        motivation_repo=motivation_repo
    )
    bot_token = ""
    bot = Bot(bot_token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    # Передача сервисов через middleware
    dp.update.middleware.register(InjectMiddleware({
        "user_service": user_service,
        "reminder_service": reminder_service,
        "notification_service": notification_service
    }))

    await dp.start_polling(bot)


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
