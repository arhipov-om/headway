import asyncio
import logging

from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand, ErrorEvent, ReplyKeyboardRemove
from aiogram_dialog import setup_dialogs, DialogManager, StartMode, ShowMode
from aiogram_dialog.api.exceptions import UnknownIntent
from environs import Env

from headway.application.services import UserService, ReminderService
from headway.infrastructure.database.inmemory import (UserRepository, InMemoryDB, ReminderRepository)
from headway.presentation.telegram import states
from headway.presentation.telegram.dialogs import start_menu, create_reminder, manage_reminder
from .handlers import router


class InjectMiddleware(BaseMiddleware):
    def __init__(self, data: dict) -> None:
        self.data = data

    async def __call__(self, handler, event, data):
        for k, v in self.data.items():
            data[k] = v
        return await handler(event, data)

class InjectUserMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        pass
    async def __call__(self, handler, event, data):
        if event.event_type == "message" or event.event_type == "callback_query":
            user_service: UserService = data['user_service']
            from_user = data.get("event_from_user")
            user = await user_service.get_user_by_identity(provider='telegram', provider_id=str(from_user.id))
            if not user:
                user = await user_service.create_user(
                    name=from_user.full_name,
                    provider='telegram',
                    provider_id=str(from_user.id)
                )

            data['user'] = user
        return await handler(event, data)

async def on_unknown_intent(event: ErrorEvent, dialog_manager: DialogManager):
    # Example of handling UnknownIntent Error and starting new dialog.
    logging.error("Restarting dialog: %s", event.exception)
    if event.update.callback_query:
        await event.update.callback_query.answer(
            "Bot process was restarted due to maintenance.\n"
            "Redirecting to main menu.",
        )
        if event.update.callback_query.message:
            try:
                await event.update.callback_query.message.delete()
            except TelegramBadRequest:
                pass  # whatever
    elif event.update.message:
        await event.update.message.answer(
            "Bot process was restarted due to maintenance.\n"
            "Redirecting to main menu.",
            reply_markup=ReplyKeyboardRemove(),
        )
    await dialog_manager.start(
        states.MainMenu.START,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.SEND,
    )


async def main():
    env = Env()
    env.read_env()

    bot_token = env.str("BOT_TOKEN")

    db = InMemoryDB()

    user_repo = UserRepository(db)
    reminder_repo = ReminderRepository(db)

    user_service = UserService(user_repo=user_repo)

    reminder_service = ReminderService(reminder_repo=reminder_repo)
    bot = Bot(bot_token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        router,
        start_menu,
        create_reminder,
        manage_reminder
    )

    dp.update.middleware.register(InjectMiddleware({
        "user_service": user_service,
        "reminder_service": reminder_service,
    }))
    dp.update.middleware.register(InjectUserMiddleware())
    dp.errors.register(
        on_unknown_intent,
        ExceptionTypeFilter(UnknownIntent),
    )

    setup_dialogs(dp)
    await bot.set_my_commands(commands=[
        BotCommand(command="/start", description='Главное меню'),
        BotCommand(command="/menu", description='Главное меню')
    ])
    await dp.start_polling(bot)


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
