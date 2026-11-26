"""Автоматические тесты модуля хранения состояния."""

from datetime import date
import pytest
from src.storage import HabitStorage, StorageError


def test_first_run_empty_state(tmp_path):
    file_path = tmp_path / "habits.json"
    storage = HabitStorage(str(file_path))
    assert storage.get_all() == []
    assert not file_path.exists()


def test_persistence_across_restart(tmp_path):
    file_path = tmp_path / "habits.json"
    storage1 = HabitStorage(str(file_path))
    storage1.add_habit("Прогулка", 7)
    storage1.add_habit("Зарядка", 14)
    storage1.mark_completed(1, completion_date=date(2026, 11, 20))

    storage2 = HabitStorage(str(file_path))
    habits = storage2.get_all()
    assert len(habits) == 2

    h1 = storage2.get_by_id(1)
    assert h1["name"] == "Прогулка"
    assert h1["completed_days"] == 1
    assert h1["streak"] == 1
    assert h1["last_completed_date"] == date(2026, 11, 20)

    h2 = storage2.get_by_id(2)
    assert h2["name"] == "Зарядка"
    assert h2["completed_days"] == 0
    assert h2["streak"] == 0


def test_streak_and_duplicate_day_logic(tmp_path):
    file_path = tmp_path / "habits.json"
    storage = HabitStorage(str(file_path))
    storage.add_habit("Чтение", 10)

    res1 = storage.mark_completed(1, completion_date=date(2026, 11, 10))
    assert res1["status"] == "completed"
    assert res1["habit"]["streak"] == 1

    res_dup = storage.mark_completed(1, completion_date=date(2026, 11, 10))
    assert res_dup["status"] == "already_completed_today"
    assert res_dup["habit"]["completed_days"] == 1

    res2 = storage.mark_completed(1, completion_date=date(2026, 11, 11))
    assert res2["status"] == "completed"
    assert res2["habit"]["streak"] == 2

    res_skip = storage.mark_completed(1, completion_date=date(2026, 11, 15))
    assert res_skip["status"] == "completed"
    assert res_skip["habit"]["streak"] == 1
    assert res_skip["habit"]["completed_days"] == 3


def test_mark_completed_not_found(tmp_path):
    storage = HabitStorage(str(tmp_path / "habits.json"))
    res = storage.mark_completed(999)
    assert res["status"] == "not_found"
    assert res["habit"] is None


def test_load_corrupted_json_raises(tmp_path):
    file_path = tmp_path / "broken.json"
    file_path.write_text("{broken json", encoding="utf-8")
    with pytest.raises(StorageError):
        HabitStorage(str(file_path))


def test_load_invalid_structure_raises(tmp_path):
    file_path = tmp_path / "invalid.json"
    file_path.write_text('{"wrong_key": []}', encoding="utf-8")
    with pytest.raises(StorageError):
        HabitStorage(str(file_path))
