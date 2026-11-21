"""Модуль хранения данных и состояния агента привычек."""

from datetime import date, timedelta
from typing import Dict, List, Optional


class HabitStorage:
    """Управление состоянием трекера привычек в памяти."""

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
            "last_completed_date": None,
        }
        self._habits[self._next_id] = habit
        self._next_id += 1
        return habit

    def get_all(self) -> List[dict]:
        return list(self._habits.values())

    def get_by_id(self, habit_id: int) -> Optional[dict]:
        return self._habits.get(habit_id)

    def mark_completed(
        self, habit_id: int, completion_date: Optional[date] = None
    ) -> dict:
        habit = self.get_by_id(habit_id)
        if habit is None:
            return {"status": "not_found", "habit": None}

        today = completion_date or date.today()
        last_date: Optional[date] = habit["last_completed_date"]

        if last_date == today:
            return {"status": "already_completed_today", "habit": habit}

        if last_date == today - timedelta(days=1):
            habit["streak"] += 1
        else:
            habit["streak"] = 1

        habit["completed_days"] += 1
        habit["last_completed_date"] = today
        return {"status": "completed", "habit": habit}
