"""Модуль логики обработки операций над привычками."""

from datetime import date
from typing import List, Optional
from src.storage import HabitStorage


class HabitAgent:
    """Бизнес-логика агента по управлению привычками."""

    def __init__(self, storage: HabitStorage) -> None:
        self.storage = storage

    def create_habit(self, name: str, target_days: int) -> dict:
        clean_name = name.strip()
        if not clean_name:
            raise ValueError("Название не может быть пустым.")
        if target_days <= 0:
            raise ValueError("Цель в днях должна быть > 0.")
        return self.storage.add_habit(clean_name, target_days)

    def list_habits(self) -> List[dict]:
        return self.storage.get_all()

    def complete_habit(
        self, habit_id: int, completion_date: Optional[date] = None
    ) -> dict:
        if habit_id <= 0:
            raise ValueError("ID должен быть больше 0.")
        return self.storage.mark_completed(habit_id, completion_date)
