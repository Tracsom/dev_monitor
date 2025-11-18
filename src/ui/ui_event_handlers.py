# src/ui/ui_event_handlers.py
"""
Event handlers for scheduler events.
"""
import logging
from typing import Callable, Optional
from tkinter import Tk, StringVar
from src.bus import Scheduler
from src.ui.dialogue_manager import DialogManager

logger = logging.getLogger(__name__)


class UIEventHandlers:
    """Manages scheduler event subscriptions for the UI."""

    def __init__(
        self, 
        scheduler: Scheduler, 
        parent: Tk, 
        refresh_callback: Callable,
        status_var: Optional[StringVar] = None
    ):
        """
        Initialize event handlers.

        Args:
            scheduler: Event scheduler
            parent: Parent Tkinter window
            refresh_callback: Function to call refresh device list
        """
        self.scheduler = scheduler
        self.parent = parent
        self.refresh_callback = refresh_callback
        self.status_var = status_var
        self._subscribe_to_events()
        logger.info("UI event handlers initialized")

    def _subscribe_to_events(self) -> None:
        """Subscribe to all relevent scheduler events."""
        self.scheduler.subscribe("device_added", self._on_device_added)
        self.scheduler.subscribe("device_add_failed", self._on_device_add_failed)
        self.scheduler.subscribe("device_removed", self._on_device_removed)
        self.scheduler.subscribe("device_remove_failed", self._on_device_remove_failed)
        self.scheduler.subscribe("devices_checked", self._on_devices_checked)
        logger.debug("UI event handlers subscribed")

    def _on_device_added(self, device_name: str) -> None:
        """Handle successful device add."""
        DialogManager.show_success(
            "Device added", 
            f"Added device {device_name}",
            status_var=self.status_var,
            modal=False
        )
        self.refresh_callback()

    def _on_device_add_failed(self, device_name: str) -> None:
        """Handle failed device add."""
        DialogManager.show_error(
            "Add failed", 
            f"Failed to add device: {device_name}",
            status_var=self.status_var,
            parent=self.parent,
            modal=True
        )

    def _on_device_removed(self, device_name: str) -> None:
        """Handle successful device removal."""
        DialogManager.show_success(
            "Device removed", 
            f"Removed device: {device_name}",
            status_var=self.status_var,
            modal=False
        )
        self.refresh_callback()

    def _on_device_remove_failed(self, device_name: str) -> None:
        """Handle failed device removal."""
        DialogManager.show_error(
            "Remove failed",
            f"Failed to remove device: {device_name}",
            status_var=self.status_var,
            parent=self.parent,
            modal=True,
        )

    def _on_devices_checked(self, device_name: str) -> None:
        """
        Handle devices checked.

        Controller publishes the full devices list; simply refresh UI.
        """
        self.refresh_callback()
