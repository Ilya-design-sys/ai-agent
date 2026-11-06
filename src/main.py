"""Точка входа: консольный интерфейс взаимодействия с пользователем."""

import sys
from src.storage import HabitStorage
from src.agent import HabitAgent


def print_help() -> None:
    """Вывод справочной информации по доступным командам."""
    print("\nДоступные команды:")
    print("  add <название> <дней> — добавить новую привычку и цель в днях")
    print("  list                  — показать все привычки и текущий прогресс")
    print("  done <id>             — отметить привычку выполненной за сегодня")
    print("  help                  — вывести эту справку")
    print("  exit                  — штатно завершить работу приложения\n")


def handle_add(agent: HabitAgent, args: list) -> None:
    if len(args) < 2:
        print(
              "Ошибка: укажите название "
              "привычки и цель. Пример: add Чтение 21"
        )
        return
    try:
        target_days = int(args[-1])
        name = " ".join(args[:-1])
        habit = agent.create_habit(name, target_days)
        msg = (
            f"Привычка '{habit['name']}' успешно добавлена "
            f"с ID: {habit['id']} (цель: {habit['target_days']} дн.)."
        )
        print(msg)
    except ValueError as err:
        print(f"Ошибка валидации данных: {err}")


def handle_list(agent: HabitAgent) -> None:
    habits = agent.list_habits()
    if not habits:
        print("Список привычек пуст. Добавьте новую командой 'add'.")
        return
    print("\nВаши текущие привычки:")
    for h in habits:
        line = (
            f"[{h['id']}] {h['name']} | "
            f"Выполнено: {h['completed_days']}/{h['target_days']} дн. | "
            f"Серия (streak): {h['streak']} дн."
        )
        print(line)
    print()


def handle_done(agent: HabitAgent, args: list) -> None:
    if not args:
        print("Ошибка: укажите ID привычки. Пример: done 1")
        return
    try:
        habit_id = int(args[0])
        updated = agent.complete_habit(habit_id)
        if updated is None:
            print(f"Ошибка: привычка с ID {habit_id} не найдена.")
        else:
            msg = (
                f"Отлично! Привычка '{updated['name']}' выполнена. "
                f"Текущая серия: {updated['streak']} дн."
            )
            print(msg)
    except ValueError:
        print("Ошибка: ID привычки должен быть целым числом.")


def main() -> None:
    storage = HabitStorage()
    agent = HabitAgent(storage)

    print("=== ИИ-Агент: Помощник по привычкам запущен ===")
    print("Введите 'help' для просмотра списка команд или 'exit' для выхода.")

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
