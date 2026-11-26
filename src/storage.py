"""Модуль хранения данных и состояния агента привычек."""

from datetime import date, timedelta
import json
from pathlib import Path
from typing import Dict, List, Optional


class StorageError(Exception):
    """Ошибка чтения или записи файла хранилища."""


class HabitStorage:
    """Управление состоянием трекера привычек с сохранением в JSON."""

    def __init__(self, file_path: str = "data/habits.json") -> None:
        self.file_path = Path(file_path)
        self._habits: Dict[int, dict] = {}
        self._next_id: int = 1
        self.load()

    def load(self) -> None:
        """Загружает состояние из JSON. При первом запуске — пустое."""
        if not self.file_path.exists():
            self._habits = {}
            self._next_id = 1
            return

        try:
            raw = self.file_path.read_text(encoding="utf-8")
            data = json.loads(raw)
        except (OSError, json.JSONDecodeError) as err:
            raise StorageError(f"Не удалось прочитать хранилище: {err}")

        if not isinstance(data, dict) or "habits" not in data:
            raise StorageError("Некорректная структура файла хранилища.")

        loaded: Dict[int, dict] = {}
        try:
            for item in data["habits"]:
                last_raw = item.get("last_completed_date")
                last_date = date.fromisoformat(last_raw) if last_raw else None
                habit_id = int(item["id"])
                loaded[habit_id] = {
                    "id": habit_id,
                    "name": str(item["name"]),
                    "target_days": int(item["target_days"]),
                    "completed_days": int(item["completed_days"]),
                    "streak": int(item["streak"]),
                    "last_completed_date": last_date,
                }
            next_id = int(data.get("next_id", len(loaded) + 1))
        except (KeyError, TypeError, ValueError) as err:
            raise StorageError(f"Повреждены данные привычек: {err}")

        self._habits = loaded
        self._next_id = max(next_id, max(loaded.keys(), default=0) + 1)

    def save(self) -> None:
        """Сохраняет текущее состояние привычек в JSON-файл."""
        serializable = []
        for habit in self._habits.values():
            last_date = habit["last_completed_date"]
            serializable.append(
                {
                    "id": habit["id"],
                    "name": habit["name"],
                    "target_days": habit["target_days"],
                    "completed_days": habit["completed_days"],
                    "streak": habit["streak"],
                    "last_completed_date": (
                        last_date.isoformat() if last_date else None
                    ),
                }
            )
        payload = {"next_id": self._next_id, "habits": serializable}
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            content = json.dumps(payload, ensure_ascii=False, indent=2)
            self.file_path.write_text(content, encoding="utf-8")
        except OSError as err:
            raise StorageError(f"Не удалось сохранить хранилище: {err}")

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
        self.save()
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
        self.save()
        return {"status": "completed", "habit": habit}
