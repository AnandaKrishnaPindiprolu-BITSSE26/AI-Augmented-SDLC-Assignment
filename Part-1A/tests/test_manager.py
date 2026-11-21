"""Tests for creating, changing, filtering, and sorting tasks."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest

from todo.exceptions import TodoError
from todo.manager import TodoManager


def test_create_list_and_ids(manager):
    first = manager.create_task("Buy milk", "2 litres", "high", ["home"])
    second = manager.create_task("Read chapter", priority="low", tags="study, uni")
    assert first.task_id == 1
    assert first.status == "pending"
    assert second.task_id == 2
    assert second.tags == ["study", "uni"]
    assert [task.task_id for task in manager.list_tasks()] == [1, 2]


def test_create_rejects_blank_title(manager):
    with pytest.raises(TodoError, match="Title is required"):
        manager.create_task("   ")


def test_update_task(manager):
    task = manager.create_task("Draft", priority="low")
    updated = manager.update_task(
        task.task_id,
        title="Final draft",
        description="Add tests",
        priority="high",
        tags=["uni"],
    )
    assert updated.title == "Final draft"
    assert updated.description == "Add tests"
    assert updated.priority == "high"
    assert updated.tags == ["uni"]


def test_invalid_priority_does_not_change_task(manager):
    task = manager.create_task("Draft", priority="low")
    with pytest.raises(TodoError, match="Priority"):
        manager.update_task(task.task_id, priority="urgent")
    saved = manager.get_task(task.task_id)
    assert saved.priority == "low"
    assert saved.title == "Draft"


def test_delete_task(manager):
    task = manager.create_task("Temp")
    deleted = manager.delete_task(task.task_id)
    assert deleted.title == "Temp"
    assert manager.list_tasks() == []


def test_delete_missing_task(manager):
    with pytest.raises(TodoError, match="not found"):
        manager.delete_task(5)


def test_mark_completed(manager):
    task = manager.create_task("Lab report")
    done = manager.mark_completed(task.task_id)
    assert done.status == "completed"
    again = manager.mark_completed(task.task_id)
    assert again.status == "completed"


def test_filter_by_tag_is_case_insensitive(manager):
    manager.create_task("Essay", tags=["Uni", "writing"])
    manager.create_task("Shop", tags=["home"])
    found = manager.filter_by_tag(" uni ")
    assert [task.title for task in found] == ["Essay"]


def test_filter_requires_a_tag(manager):
    with pytest.raises(TodoError, match="Tag is required"):
        manager.filter_by_tag("   ")


def test_sort_by_priority(manager):
    manager.create_task("Low one", priority="low")
    manager.create_task("High one", priority="high")
    manager.create_task("Medium one", priority="medium")
    manager.create_task("High two", priority="high")
    ordered = manager.sort_by_priority()
    assert [task.title for task in ordered] == [
        "High one",
        "High two",
        "Medium one",
        "Low one",
    ]


def test_sort_can_be_saved(manager):
    manager.create_task("Low one", priority="low")
    manager.create_task("High one", priority="high")
    manager.sort_by_priority(save=True)
    assert [task.title for task in manager.list_tasks()] == [
        "High one",
        "Low one",
    ]


def test_tasks_are_reloaded_from_json(tmp_path):
    path = tmp_path / "tasks.json"
    original = TodoManager(path)
    original.create_task("Persist me", tags=["save"])
    original.mark_completed(1)

    reloaded = TodoManager(path)
    task = reloaded.get_task(1)
    assert task.title == "Persist me"
    assert task.status == "completed"
    assert task.tags == ["save"]
    assert reloaded.create_task("Next").task_id == 2
