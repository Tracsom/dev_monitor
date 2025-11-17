# src/bus/event.py
"""
Event class for bus operations.
"""
from typing import Callable, Any


class Event:
    """Represents a publishable event with a callback handler."""

    def __init__(self, name: str, callback: Callable[..., Any]):
        """
        Initialize an event.

        Args:
            name: Unique event identifier
            callback: Function to call when the event is published
        """
        if not callable(callback):
            raise TypeError(f"callback must be callable, got {type(callback)}")

        self.name = name
        self.callback = callback

    def __repr__(self):
        return f"Event(name={self.name}, callback={self.callback.__name__})"

    def trigger(self, *args, **kwargs):
        """
        Trigger the event's callback with provided arguments.

        Args:
            *args: Positional arguments for the callback
            **kwargs: Keyword arguments for the callback
        """
        return self.callback(*args, **kwargs)
