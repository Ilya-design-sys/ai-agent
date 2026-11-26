"""Точка входа: консольный интерфейс взаимодействия с пользователем."""

import os
import sys
from src.agent import HabitAgent
from src.storage import HabitStorage, StorageError


def print_help() -> None:
    """Вывод справочной информации по доступным командам."""
    print("\nДоступные команды:")
    print("  add <название> <дней> — добавить привычку и цель")
    print("  list                  — показать все привычки и прогресс")
    print("  done <id>             — отметить привычку за сегодня")
    print("  help                  — вывести эту справку")
    print("  exit                  — штатно завершить работу\n")


def handle_add(agent: HabitAgent, args: list) -> None:
    if len(args) < 2:
        print("Ошибка: укажите название и цель. Пример: add Чтение 21")
        return
    try:
        target_days = int(args[-1])
        name = " ".join(args[:-1])
        habit = agent.create_habit(name, target_days)
        print(
            f"Привычка '{habit['name']}' успешно добавлена "
            f"с ID: {habit['id']} (цель: {habit['target_days']} дн.)."
        )
    except (ValueError, StorageError) as err:
        print(f"Ошибка: {err}")


def handle_list(agent: HabitAgent) -> None:
    habits = agent.list_habits()
    if not habits:
        print("Список привычек пуст. Добавьте новую командой 'add'.")
        return
    print("\nВаши текущие привычки:")
    for h in habits:
        last_mark = (
            h["last_completed_date"].isoformat()
            if h["last_completed_date"] is not None
            else "нет"
        )
        line = (
            f"[{h['id']}] {h['name']} | "
            f"Выполнено: {h['completed_days']}/{h['target_days']} дн. | "
            f"Серия (streak): {h['streak']} дн. | "
            f"Последняя отметка: {last_mark}"
        )
        print(line)
    print()


def handle_done(agent: HabitAgent, args: list) -> None:
    if len(args) != 1:
        print(
            "Ошибка: неверный формат команды done. "
            "Ожидается ровно один аргумент: done <id>"
        )
        return
    try:
        habit_id = int(args[0])
        result = agent.complete_habit(habit_id)
    except ValueError as err:
        if args[0].lstrip("-").isdigit():
            print(f"Ошибка валидации данных: {err}")
        else:
            print("Ошибка: ID привычки должен быть целым числом.")
        return
    except StorageError as err:
        print(f"Ошибка хранилища: {err}")
        return

    status = result["status"]
    habit = result["habit"]

    if status == "not_found":
        print(f"Ошибка: привычка с ID {habit_id} не найдена.")
    elif status == "already_completed_today":
        print(
            f"Привычка '{habit['name']}' уже отмечена за сегодня. "
            f"Текущая серия: {habit['streak']} дн."
        )
    elif status == "completed":
        print(
            f"Отлично! Привычка '{habit['name']}' выполнена за сегодня. "
            f"Текущая серия: {habit['streak']} дн."
        )


def main() -> None:
    storage_path = os.getenv("HABIT_STORAGE_PATH", "data/habits.json")
    try:
        storage = HabitStorage(file_path=storage_path)
    except StorageError as err:
        print(f"Ошибка загрузки состояния: {err}")
        print("Приложение продолжит работу с пустым состоянием.")
        storage = HabitStorage.__new__(HabitStorage)
        storage.file_path = storage_path
        storage._habits = {}
        storage._next_id = 1

    agent = HabitAgent(storage)

    print("=== ИИ-Агент: Помощник по привычкам запущен ===")
    print("Введите 'help' для списка команд или 'exit' для выхода.")

    while True:
        try:
            user_input = input("agent> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nЗавершение работы программы.")
            break

        if not user_input:
            continue

        parts = user_input.split()
        command = parts[0].lower()
        args = parts[1:]

        if command == "exit":
            print("Работа приложения штатно завершена. До встречи!")
            sys.exit(0)
        elif command == "help":
            print_help()
        elif command == "add":
            handle_add(agent, args)
        elif command == "list":
            handle_list(agent)
        elif command == "done":
            handle_done(agent, args)
        else:
            print(
                f"Неизвестная команда '{command}'. "
                "Введите 'help' для списка доступных команд."
            )


if __name__ == "__main__":
    main()
