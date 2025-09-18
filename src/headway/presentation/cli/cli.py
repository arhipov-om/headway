import asyncio
import sys
from datetime import time
from uuid import UUID

from dishka import make_async_container
from environs import Env

from headway.application.dto import (
    UserDTO,
    ReminderDTO,
    CreateReminderDTO,
)
from headway.application.services import UserService, ReminderService
from headway.infrastructure.di import get_providers


class CLI:

    def __init__(self, user_service: UserService, reminder_service: ReminderService):
        self._user_id: None | UUID = None
        self.user_service = user_service
        self.reminder_service = reminder_service

        self.actions = {
            "1": ("Создать пользователя", self.create_user),
            "2": ("Создать напоминание", self.create_reminder),
            "3": ("Список напоминаний", self.list_reminders),
            "q": ("Выход", sys.exit),
        }

    @property
    def user_id(self):
        return self._user_id

    async def create_user(self):
        user_dto = await self.user_service.get_user_by_identity(provider="cli", provider_id="1")
        if not user_dto:
            name = input("Введите имя пользователя: ")
            user_dto: UserDTO = await self.user_service.create_user(name=name, provider='cli', provider_id="1")
        self._user_id = user_dto.id
        print(f"Пользователь создан: {user_dto.id} - {user_dto.name}")

    async def create_reminder(self):
        # user_id_input = input("ID пользователя: ")
        # user_id = UUID(user_id_input)
        text = input("Текст напоминания: ")
        frequency = input("Частота (daily/every_2_days/weekly/custom): ")
        t_input = input("Время (ЧЧ:ММ): ")
        h, m = map(int, t_input.split(":"))
        t = time(h, m)
        duration = input("Длительность (1w/2w/1m/3m/6m/12m): ")

        reminder_dto: ReminderDTO = await self.reminder_service.create_reminder(
            CreateReminderDTO(
                user_id=self.user_id,
                text=text,
                frequency=frequency,
                time=t,
                duration=duration,
                days="",
            )
        )
        print(f"Напоминание создано: {reminder_dto.id} - {reminder_dto.text}")

    async def list_reminders(self):
        # user_id_input = input("ID пользователя для просмотра напоминаний: ")
        # user_id = UUID(user_id_input)
        reminders: list[ReminderDTO] = await self.reminder_service.list_reminders_by_user(self.user_id)
        for r in reminders:
            print(f"{r.id} | {r.text} | {r.frequency} | {r.time} | Активно: {r.active}")

    async def run(self):
        while True:
            print("\nВыберите действие:")
            for k, v in self.actions.items():
                print(f"{k}: {v[0]}")
            choice = input("> ").strip()
            if choice in self.actions:
                try:
                    await self.actions[choice][1]()
                except Exception as e:
                    print(e)
            else:
                print("Неверный выбор!")


async def main():
    env = Env()
    env.read_env()
    container = make_async_container(*get_providers(), context={Env: env})
    async with container() as scope:
        user_service = await scope.get(UserService)
        reminder_service = await scope.get(ReminderService)

        cli = CLI(user_service, reminder_service)
        await cli.run()


def run():
    asyncio.run(main())
