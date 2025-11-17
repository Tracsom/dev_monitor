# src/bus/scheduler.py
"""
Scheduler module for bus operations.
Implements a simple publish-subscribe pattern.
"""
import logging
from typing import Callable, Any, List
from src.bus.event import Event

logger = logging.getLogger(__name__)


class Scheduler:
    """Event bus for application communication."""

    def __init__(self):
        """Initialize the event scheduler."""
        self._events: List[Event] = []

    def subscribe(self, event_name: str, callback: Callable[..., Any]) -> None:
        """
        Subscribe to an event.

        Args:
            event_name: Name of event to subscribe to
            callback: Function to call when the event is published

        Raises:
            TypeError: If callback is not callable
        """
        if not callable(callback):
            raise TypeError(f"callback must be callable, got {type(callback)}")

        event = Event(event_name, callback)
        self._events.append(event)
        logger.debug(f"Subscribed to event: {event_name}")

    def unsubscribe(
        self, event_name: str, callback: Callable[..., Any]
    ) -> bool:
        """
        Unsubscribe from an event.

        Args:
            event_name: Name of event to unsubscribe from
            callback: Callback to remove

        Returns:
            True if successfully unsubscribed, False otherwise
        """
        original_count = len(self._events)
        self._events = [
            e
            for e in self._events
            if not (e.name == event_name and e.callback == callback)
        ]
        removed = len(self._events) < original_count
        if removed:
            logger.debug(f"Unsubscribed from event: {event_name}")
        return removed

    def publish(self, event_name: str, *args, **kwargs) -> List[Any]:
        """
        Publish an event to all subscribers.

        Args:
            event_name: Name of event to publish
            *args: Positional arguments for the callback
            **kwargs: Keyword arguments for the callback

        Returns:
            List of return values from all callbacks
        """
        results: List[Any] = []
        matching_events = [e for e in self._events if e.name == event_name]

        if not matching_events:
            logger.debug(f"Event published with no subscribers: {event_name}")
            return results

        logger.debug(
            f"Publishing event: {event_name} to {len(matching_events)} subscriber(s)"
        )

        for event in matching_events:
            try:
                result = event.trigger(*args, **kwargs)
                results.append(result)
            except Exception as e:
                logger.error(
                    f"Error in event callback for {event_name}: {e}",
                    exc_info=True,
                )

        return results

    def __repr__(self) -> str:
        return f"Scheduler(events={len(self._events)})"
