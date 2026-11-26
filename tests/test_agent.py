"""Автоматические тесты бизнес-логики агента."""

from datetime import date
import pytest
from src.agent import HabitAgent
from src.storage import HabitStorage


def test_create_and_list_habits(tmp_path):
    storage = HabitStorage(str(tmp_path / "habits.json"))
    agent = HabitAgent(storage)

    habit = agent.create_habit("  Спорт  ", 30)
    assert habit["id"] == 1
    assert habit["name"] == "Спорт"
    assert habit["target_days"] == 30
    assert len(agent.list_habits()) == 1


def test_create_habit_validation_errors(tmp_path):
    storage = HabitStorage(str(tmp_path / "habits.json"))
    agent = HabitAgent(storage)

    with pytest.raises(ValueError):
        agent.create_habit("   ", 10)

    with pytest.raises(ValueError):
        agent.create_habit("Бег", 0)

    with pytest.raises(ValueError):
        agent.create_habit("Бег", -5)


def test_complete_habit_and_validation(tmp_path):
    storage = HabitStorage(str(tmp_path / "habits.json"))
    agent = HabitAgent(storage)
    agent.create_habit("Вода", 7)

    with pytest.raises(ValueError):
        agent.complete_habit(0)

    res = agent.complete_habit(1, completion_date=date(2026, 11, 20))
    assert res["status"] == "completed"
    assert res["habit"]["streak"] == 1
