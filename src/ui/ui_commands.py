# src/ui/ui_commands.py
"""
Command handlers for UI actions.
"""
import logging
import threading
from typing import Callable, Optional
from tkinter import Tk, StringVar
from src.bus import Scheduler
from src.ui.dialogue_manager import DialogManager
from src.ui.progress_manager import ProgressManager

logger = logging.getLogger(__name__)


class UICommands:
    """Handles all user commands from buttons."""

    def __init__(
        self,
        scheduler: Scheduler,
        parent: Tk,
        status_var: StringVar,
        refresh_callback: Callable,
        progress_manager: Optional["ProgressManager"] = None,
        disable_buttons_callback: Optional[Callable[[bool], None]] = None
    ):
        """
        Initialize command handler.

        Args:
            scheduler: Event scheduler
            parent: Parent tkinter window
            status_var: StringVar for status display
            refresh_callback: Function to refresh device list
            progress_manager: Optional progess manager for feedback
            disable_buttons_callback: Optional callback to disable/enable buttons
        """
        self.scheduler = scheduler
        self.parent = parent
        self.status_var = status_var
        self.refresh_callback = refresh_callback
        self.progress_manager = progress_manager
        self.disable_buttons_callback = disable_buttons_callback

    def add_device(self) -> None:
        """Handle add device command."""
        device_details = DialogManager.ask_device_details(self.parent)
        if not device_details:
            return

        name, ip, port, timeout = device_details
        self.status_var.set("Adding device...")
        self.scheduler.publish("add_device", name, ip, port, timeout)

    def remove_device(
        self, get_selected_name: Callable[[], Optional[str]]
    ) -> None:
        """
        Handle remove device command.

        Args:
            get_selected_name: Function that returns selected device name
        """
        device_name = get_selected_name()
        if not device_name:
            DialogManager.show_warning(
                "Remove device", 
                "No device selected",
                status_var=self.status_var,
                parent=self.parent,
                modal=False
            )
            return

        if not DialogManager.confirm_remove(self.parent, device_name):
            return

        self.status_var.set(f"Removing {device_name}...")
        self.scheduler.publish("remove_device", device_name)

    def check_all(self) -> None:
        """Handle check all devices command."""
        # Confirm if there are many devices to avoid accidental log operations
        devices = self.scheduler.publish("get_devices")
        count = 0
        if devices and isinstance(devices[0], list):
            count = len(devices)
        if count > 50:
            if not DialogManager.confirm_remove(self.parent, f"Run checks on {count} devices?"):
                return
        def worker():
            # show progress and disable buttons
            if self.progress_manager:
                self.parent.after(
                    10,
                    lambda: self.progress_manager.show("Checking all devices..."),
                )
            if self.disable_buttons_callback:
                self.parent.after(10, lambda: self.disable_buttons_callback(True))

            self.status_var.set("Checking devices...")
            self.scheduler.publish("check_all_devices")
            
            # Hide progress and re-enable buttons when done
            if self.progress_manager:
                self.parent.after(50, lambda: self.progress_manager.hide())
            if self.disable_buttons_callback:
                self.parent.after(50, lambda: self.disable_buttons_callback(False))
            self.parent.after(50, lambda: self.status_var.set("Check complete"))

        threading.Thread(target=worker, daemon=True).start()

    def refresh(self) -> None:
        """Handle refresh command."""
        self.status_var.set("Refreshing device list...")
        self.refresh_callback()
        self.status_var.set("Device list refreshed")
