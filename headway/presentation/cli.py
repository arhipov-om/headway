import sys
from datetime import time
from uuid import UUID

from headway.application.dto import UserDTO, ReminderDTO, NotificationDTO
from headway.application.services import UserService, ReminderService, NotificationService
from headway.infrastructure.inmemory import InMemoryDB, UserRepository, ReminderRepository, NotificationRepository, \
    MotivationRepository


class CLI:
    def __init__(self,
                 user_service: UserService,
                 reminder_service: ReminderService,
                 notification_service: NotificationService):
        self.user_service = user_service
        self.reminder_service = reminder_service
        self.notification_service = notification_service

    def create_user(self):
        name = input("Введите имя пользователя: ")
        user_dto: UserDTO = self.user_service.create_user(name)
        print(f"Пользователь создан: {user_dto.id} - {user_dto.name}")

    def create_reminder(self):
        user_id_input = input("ID пользователя: ")
        user_id = UUID(user_id_input)
        text = input("Текст напоминания: ")
        frequency = input("Частота (daily/every_2_days/weekly/custom): ")
        t_input = input("Время (ЧЧ:ММ): ")
        h, m = map(int, t_input.split(":"))
        t = time(h, m)
        duration = input("Длительность (1w/2w/1m/3m/6m/12m): ")

        reminder_dto: ReminderDTO = self.reminder_service.create_reminder(user_id, text, frequency, t, duration)
        print(f"Напоминание создано: {reminder_dto.id} - {reminder_dto.text}")

    def list_reminders(self):
        user_id_input = input("ID пользователя для просмотра напоминаний: ")
        user_id = UUID(user_id_input)
        reminders: list[ReminderDTO] = self.reminder_service.list_reminders_by_user(user_id)
        for r in reminders:
            print(f"{r.id} | {r.text} | {r.frequency} | {r.time} | Активно: {r.active}")

    def generate_notifications(self):
        notifications: list[NotificationDTO] = self.notification_service.generate_notifications()
        for n in notifications:
            print(f"Notification для '{n.reminder_id}' с мотивацией: '{n.motivation_text}' создан")

    def list_notifications(self):
        notifications: list[NotificationDTO] = self.notification_service.list_notifications()
        for n in notifications:
            print(f"{n.id} | Напоминание: {n.reminder_id} | Мотивация: {n.motivation_text} | Отправлено: {n.sent}")


def main():
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

    cli = CLI(user_service, reminder_service, notification_service)

    actions = {
        "1": ("Создать пользователя", cli.create_user),
        "2": ("Создать напоминание", cli.create_reminder),
        "3": ("Список напоминаний", cli.list_reminders),
        "4": ("Сгенерировать уведомления с мотивацией", cli.generate_notifications),
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
