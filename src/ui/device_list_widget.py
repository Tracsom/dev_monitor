# src/ui/device_list_widget.py
"""
Custom Tkinter widgets for the application
"""
import logging
from tkinter import Listbox, Frame
from tkinter.ttk import Scrollbar
from typing import List, Optional, Callable
from src.models import Device

logger = logging.getLogger(__name__)

class DeviceListWidget(Frame):
    """Custom widget for displaying devices in a scrollable list."""

    def __init__(self, parent, height: int = 12, width: int = 60, **kwargs):
        """
        Initialize device list widget.

        Args:
            parent: Parent widget
            height: Number of visible rows
            width: Width in characters
            **kwargs: Additional frame arguments
        """
        super().__init__(parent, **kwargs)

        self.listbox = Listbox(self, height=height, width=width)
        self.listbox.grid(row=0, column=0, sticky="nsew", padx=(0, 8))

        scrollbar = Scrollbar(self, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=scrollbar.set)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def populate(self, devices: List[Device]) -> None:
        """
        Populate list with devices.

        Args:
            devices: List of Device objects
        """
        self.listbox.delete(0, "end")
        for device in devices:
            line = self._format_device_line(device)
            self.listbox.insert("end", line)
        logger.debug(f"Populated device list with {len(devices)} devices")

    def get_selected_device_name(self) -> Optional[str]:
        """
        Get name of selected device.

        Returns:
            Device name or None if nothing selected
        """
        selection = self.listbox.curselection()
        if not selection:
            return None
        
        line = self.listbox.get(selection[0])
        parts = line.split(" - ")
        return parts[0] if parts else None
    
    def bind_double_click(self, callback: Callable) -> None:
        """
        Bind callback to double-click event.

        Args:
            callback: Function to call on double-click
        """
        self.listbox.bind("<Double-Button-1>", lambda e: callback())

    @staticmethod
    def _format_device_line(device: Device) -> str:
        """Format device for display in list."""
        status = "Online" if device.is_online else "Offline" if device.is_online is False else "Unknown"
        return f"{device.name} - {device.ip_address}:{device.port} - {status} - Last checked: {device.last_checked or 'never'}"