from datetime import datetime

from src.reminder_agent import ReminderAgent


REFERENCE = datetime(2026, 11, 21, 12, 0, 0)


def test_create_reminder():
    response = ReminderAgent().process("Remind me to call mom tomorrow at 5 PM", REFERENCE)
    assert response["intent"] == "create_reminder"
    assert response["task"] == "call mom"
    assert response["datetime"] == "2026-11-22T17:00:00"
    assert response["needs_clarification"] is False


def test_missing_time_requires_clarification():
    response = ReminderAgent().process("Remind me about the meeting", REFERENCE)
    assert response["intent"] == "clarification_required"
    assert response["datetime"] is None
    assert response["needs_clarification"] is True


def test_invalid_date_requires_clarification():
    response = ReminderAgent().process("Remind me to file taxes on February 30 at 9 AM", REFERENCE)
    assert response["intent"] == "clarification_required"
    assert response["datetime"] is None


def test_empty_input_requires_clarification():
    response = ReminderAgent().process("", REFERENCE)
    assert response["intent"] == "clarification_required"
