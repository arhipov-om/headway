import sys
from datetime import time, datetime
from uuid import uuid4, UUID

from headway.infrastructure.inmemory import InMemoryDB
from ..domain.entitites import User, Reminder, Motivation, Notification


class CLI:
    def __init__(self, database: InMemoryDB):
        self.database = database

    def create_user(self):
        name = input("Введите имя пользователя: ")
        user = User(id=uuid4(), name=name)
        self.database.users[user.id] = user
        print(f"Пользователь создан: {user.id} - {user.name}")

    def create_reminder(self):
        user_id_input = input("ID пользователя: ")
        user_id = UUID(user_id_input)
        text = input("Текст напоминания: ")
        frequency = input("Частота (daily/every_2_days/weekly/custom): ")
        t_input = input("Время (ЧЧ:ММ): ")
        h, m = map(int, t_input.split(":"))
        t = time(h, m)
        duration = input("Длительность (1w/2w/1m/3m/6m/12m): ")
        reminder = Reminder(id=uuid4(), user_id=user_id, text=text, frequency=frequency, time=t, duration=duration)
        self.database.reminders[reminder.id] = reminder
        print(f"Напоминание создано: {reminder.id} - {reminder.text}")

    def list_reminders(self):
        for r in self.database.reminders.values():
            user = self.database.users[r.user_id]
            print(f"{r.id} | {r.text} | {r.frequency} | {r.time} | Пользователь: {user.name}")

    def generate_notification(self):
        for reminder in self.database.reminders.values():
            motivation = Motivation(id=uuid4(), text=f"Аффирмация для {reminder.text}")
            self.database.motivations[motivation.id] = motivation
            notification = Notification(
                id=uuid4(),
                reminder_id=reminder.id,
                scheduled_for=datetime.now(),
                motivation_id=motivation.id
            )
            self.database.notifications[notification.id] = notification
            print(f"Notification для '{reminder.text}' с мотивацией: '{motivation.text}' создан")

    def list_notifications(self):
        for n in self.database.notifications.values():
            r = self.database.reminders[n.reminder_id]
            m = self.database.motivations[n.motivation_id]
            print(f"{n.id} | Напоминание: {r.text} | Мотивация: {m.text} | Отправлено: {n.sent}")


def main():
    db = InMemoryDB()
    cli = CLI(db)
    actions = {
        "1": ("Создать пользователя", cli.create_user),
        "2": ("Создать напоминание", cli.create_reminder),
        "3": ("Список напоминаний", cli.list_reminders),
        "4": ("Сгенерировать уведомления с мотивацией", cli.generate_notification),
        "5": ("Список уведомлений", cli.list_notifications),
        "q": ("Выход", sys.exit)
    }

    while True:
        print("\nВыберите действие:")
        for k, v in actions.items():
            print(f"{k}: {v[0]}")
        choice = input("> ").strip()
        if choice in actions:
            try:
                actions[choice][1]()
            except Exception as e:
                print(e)
        else:
            print("Неверный выбор!")


if __name__ == "__main__":
    main()
