import asyncio
import sys
from datetime import time
from uuid import UUID

from headway.application.dto import (
    UserDTO,
    ReminderDTO,
    CreateReminderDTO,
)
from headway.application.services import UserService, ReminderService
from headway.application.value_objects import Duration
from headway.domain.entitites import Frequency
from headway.infrastructure.inmemory import InMemoryDB, UserRepository, ReminderRepository


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

    async def create_user(self):
        name = input("Введите имя пользователя: ")
        user_dto: UserDTO = await self.user_service.create_user(name)
        self._user_id = user_dto.id
        print(f"Пользователь создан: {user_dto.id} - {user_dto.name}")

    async def create_reminder(self):
        user_id_input = input("ID пользователя: ")
        user_id = UUID(user_id_input)
        text = input("Текст напоминания: ")
        frequency = input("Частота (daily/every_2_days/weekly/custom): ")
        t_input = input("Время (ЧЧ:ММ): ")
        h, m = map(int, t_input.split(":"))
        t = time(h, m)
        duration = input("Длительность (1w/2w/1m/3m/6m/12m): ")

        reminder_dto: ReminderDTO = await self.reminder_service.create_reminder(
            CreateReminderDTO(
                user_id=user_id,
                text=text,
                frequency=Frequency(frequency),
                time=t,
                duration=Duration(duration),
            )
        )
        print(f"Напоминание создано: {reminder_dto.id} - {reminder_dto.text}")

    async def list_reminders(self):
        user_id_input = input("ID пользователя для просмотра напоминаний: ")
        user_id = UUID(user_id_input)
        reminders: list[ReminderDTO] = await self.reminder_service.list_reminders_by_user(user_id)
        for r in reminders:
            print(f"{r.id} | {r.text} | {r.frequency.value} | {r.time} | Активно: {r.active}")

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
    db = InMemoryDB()

    user_repo = UserRepository(db)
    reminder_repo = ReminderRepository(db)

    user_service = UserService(user_repo=user_repo)
    reminder_service = ReminderService(reminder_repo=reminder_repo)

    cli = CLI(user_service, reminder_service)
    await cli.run()

def run():
    asyncio.run(main())
