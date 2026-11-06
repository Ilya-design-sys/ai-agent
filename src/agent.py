"""Модуль логики обработки операций над привычками."""

from typing import List, Optional
from src.storage import HabitStorage


class HabitAgent:
    """Бизнес-логика ИИ-агента по управлению привычками."""

    def __init__(self, storage: HabitStorage) -> None:
        self.storage = storage

    def create_habit(self, name: str, target_days: int) -> dict:
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Название привычки не может быть пустым.")
        if target_days <= 0:
            raise ValueError(
                "Целевое количество дней должно быть положительным числом."
            )
        return self.storage.add_habit(clean_name, target_days)

    def list_habits(self) -> List[dict]:
        return self.storage.get_all()

    def complete_habit(self, habit_id: int) -> Optional[dict]:
        if habit_id <= 0:
            raise ValueError("Идентификатор привычки должен быть больше нуля.")
        return self.storage.mark_completed(habit_id)
