"""Shared test setup."""

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from todo.manager import TodoManager  # noqa: E402


@pytest.fixture
def manager(tmp_path):
    """Return a manager that stores tasks in a temporary file."""
    return TodoManager(tmp_path / "tasks.json")
