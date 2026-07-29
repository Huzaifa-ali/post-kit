"""Tests for the event bus."""

from backend.core import events


def test_emit_calls_listener():
    received = []
    events.on("test.event", lambda data: received.append(data))
    events.emit("test.event", {"key": "value"})
    assert received == [{"key": "value"}]
    events.clear()


def test_emit_with_no_data():
    received = []
    events.on("test.empty", lambda data: received.append(data))
    events.emit("test.empty")
    assert received == [{}]
    events.clear()


def test_multiple_listeners():
    results = []
    events.on("test.multi", lambda d: results.append("a"))
    events.on("test.multi", lambda d: results.append("b"))
    events.emit("test.multi")
    assert results == ["a", "b"]
    events.clear()


def test_emit_handles_listener_error():
    """Failing listener doesn't crash emit."""

    def bad_listener(data):
        raise ValueError("broken")

    events.on("test.fail", bad_listener)
    events.emit("test.fail", {})  # Should not raise
    events.clear()


def test_clear_removes_all_listeners():
    events.on("test.clear", lambda d: None)
    events.clear()
    # Emit after clear should do nothing (no error)
    events.emit("test.clear", {"data": 1})
