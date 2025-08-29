import asyncio

from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.fsm.storage.memory import MemoryStorage
from environs import Env

from headway.application.services import UserService, ReminderService
from headway.infrastructure.inmemory import (UserRepository, InMemoryDB, ReminderRepository)
from .handlers import router


class InjectMiddleware(BaseMiddleware):
    def __init__(self, data: dict) -> None:
        self.data = data

    async def __call__(self, handler, event, data):
        for k, v in self.data.items():
            data[k] = v
        return await handler(event, data)


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
    dp.include_router(router)

    dp.update.middleware.register(InjectMiddleware({
        "user_service": user_service,
        "reminder_service": reminder_service,
    }))

    await dp.start_polling(bot)


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
