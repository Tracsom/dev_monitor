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

logger = logging.getLogger(__name__)

class UICommands:
    """Handles all user commands from buttons."""

    def __init__(self, scheduler: Scheduler, parent: Tk, status_var: StringVar, refresh_callback: Callable):
        """
        Initialize command handler.

        Args:
            scheduler: Event scheduler
            parent: Parent tkinter window
            status_var: StringVar for status display
            refresh_callback: Function to refresh device list
        """
        self.scheduler = scheduler
        self.parent = parent
        self.status_var = status_var
        self.refresh_callback = refresh_callback

    def add_device(self) -> None:
        """Handle add device command."""
        device_details = DialogManager.ask_device_details(self.parent)
        if not device_details:
            return
        
        name, ip, port, timeout = device_details
        self.status_var.set("Adding device...")
        self.scheduler.publish("add_device", name, ip, port, timeout)

    def remove_device(self, get_selected_name: Callable[[], Optional[str]]) -> None:
        """
        Handle remove device command.

        Args:
            get_selected_name: Function that returns selected device name
        """
        device_name = get_selected_name()
        if not device_name:
            DialogManager.show_warning(self.parent, "Remove device", "No device selected")
            return
        
        if not DialogManager.confirm_remove(self.parent, device_name):
            return
        
        self.status_var.set(f"Removing {device_name}...")
        self.scheduler.publish("remove_device", device_name)

    def check_all(self) -> None:
        """Handle check all devices command."""
        def worker():
            self.status_var.set("Checking devices...")
            self.scheduler.publish("check_all_devices")
            if self.parent:
                self.parent.after(50, lambda: self.status_var.set("Check complete"))

        threading.Thread(target=worker, daemon=True).start()

    def refresh(self) -> None:
        """Handle refresh command."""
        self.refresh_callback()