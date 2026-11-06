"""Модуль хранения данных и состояния агента привычек."""

from typing import Dict, List, Optional


class HabitStorage:
    """Класс для управления состоянием трекера
    привычек в оперативной памяти."""

    def __init__(self) -> None:
        self._habits: Dict[int, dict] = {}
        self._next_id: int = 1

    def add_habit(self, name: str, target_days: int) -> dict:
        habit = {
            "id": self._next_id,
            "name": name,
            "target_days": target_days,
            "completed_days": 0,
            "streak": 0,
        }
        self._habits[self._next_id] = habit
        self._next_id += 1
        return habit

    def get_all(self) -> List[dict]:
        return list(self._habits.values())

    def get_by_id(self, habit_id: int) -> Optional[dict]:
        return self._habits.get(habit_id)

    def mark_completed(self, habit_id: int) -> Optional[dict]:
        habit = self.get_by_id(habit_id)
        if habit is None:
            return None
        habit["completed_days"] += 1
        habit["streak"] += 1
        return habit
