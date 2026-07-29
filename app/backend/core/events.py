"""Simple event bus — observer pattern for module communication."""

from collections import defaultdict
from typing import Any, Callable
import logging

logger = logging.getLogger(__name__)

_listeners: dict[str, list[Callable]] = defaultdict(list)


def on(event_name: str, callback: Callable) -> None:
    """Register a listener for an event."""
    _listeners[event_name].append(callback)


def emit(event_name: str, data: dict[str, Any] | None = None) -> None:
    """Emit an event to all registered listeners."""
    for callback in _listeners[event_name]:
        try:
            callback(data or {})
        except Exception as exc:
            logger.error(f"Event listener failed for '{event_name}': {exc}")


def clear() -> None:
    """Clear all listeners (for testing)."""
    _listeners.clear()
