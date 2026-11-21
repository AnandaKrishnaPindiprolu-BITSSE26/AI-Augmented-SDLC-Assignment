"""A small menu test that uses scripted answers."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from todo.cli import main


def test_cli_create_complete_and_list(tmp_path, monkeypatch, capsys):
    answers = iter(
        [
            "1",
            "Submit report",
            "Part 1A",
            "high",
            "uni, assignment",
            "5",
            "1",
            "2",
            "8",
        ]
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: next(answers))
    path = tmp_path / "tasks.json"

    exit_code = main(["--file", str(path)])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Created task 1." in output
    assert "Submit report" in output
    assert "Task 1 marked as completed." in output
    assert "Status:      completed" in output
    assert path.exists()
