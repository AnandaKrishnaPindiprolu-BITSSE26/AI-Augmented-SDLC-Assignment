"""Tests for task validation and JSON conversion."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest

from todo.exceptions import TodoError
from todo.task import Task


def test_task_round_trip_drops_duplicate_tags():
    task = Task(1, " Read ", " Chapter 2 ", "HIGH", ["study", "Study"], "pending")
    copy = Task.from_dict(task.to_dict())
    assert copy.to_dict() == task.to_dict()
    assert task.title == "Read"
    assert task.priority == "high"
    assert task.tags == ["study"]


def test_rejects_blank_title():
    with pytest.raises(TodoError, match="Title is required"):
        Task(1, "   ")


def test_rejects_bad_priority():
    with pytest.raises(TodoError, match="Priority"):
        Task(1, "Read", priority="urgent")


def test_rejects_bad_status():
    with pytest.raises(TodoError, match="Status"):
        Task(1, "Read", status="done")


def test_from_dict_missing_field():
    with pytest.raises(TodoError, match="title"):
        Task.from_dict({"task_id": 1})


def test_rejects_non_numeric_task_id():
    with pytest.raises(TodoError, match="Task ID"):
        Task("1", "Read")
