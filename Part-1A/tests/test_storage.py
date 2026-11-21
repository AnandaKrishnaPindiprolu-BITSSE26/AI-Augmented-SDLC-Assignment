"""Tests for the JSON storage file."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest

from todo.exceptions import TodoError
from todo.storage import JsonStorage
from todo.task import Task


def test_missing_file_starts_empty(tmp_path):
    tasks, next_id = JsonStorage(tmp_path / "missing.json").load()
    assert tasks == []
    assert next_id == 1


def test_empty_file_starts_empty(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text("  \n", encoding="utf-8")
    tasks, next_id = JsonStorage(path).load()
    assert tasks == []
    assert next_id == 1


def test_save_and_load_round_trip(tmp_path):
    path = tmp_path / "nested" / "tasks.json"
    storage = JsonStorage(path)
    tasks = [Task(1, "One", "desc", "medium", ["a"], "pending")]
    storage.save(tasks, 2)
    loaded, next_id = storage.load()
    assert next_id == 2
    assert loaded[0].to_dict() == tasks[0].to_dict()
    saved = json.loads(path.read_text(encoding="utf-8"))
    assert saved["next_id"] == 2
    assert saved["tasks"][0]["title"] == "One"


def test_invalid_json(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text("[", encoding="utf-8")
    with pytest.raises(TodoError, match="invalid JSON"):
        JsonStorage(path).load()


def test_next_id_moves_past_existing_tasks(tmp_path):
    path = tmp_path / "tasks.json"
    path.write_text(
        json.dumps(
            {
                "next_id": 1,
                "tasks": [
                    {
                        "task_id": 4,
                        "title": "Old",
                        "description": "",
                        "priority": "low",
                        "tags": [],
                        "status": "pending",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    tasks, next_id = JsonStorage(path).load()
    assert tasks[0].task_id == 4
    assert next_id == 5
