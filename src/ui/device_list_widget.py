# src/ui/device_list_widget.py
"""
Custom Tkinter widgets for the application
"""
import logging
from tkinter import Listbox, Frame, Scrollbar
from tkinter.ttk import Scrollbar as TtkScrollbar
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
        """
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.height = height
        self.width = width
        self.selected_index: Optional[int] = None

        # Create listbox with scrollbar
        scrollbar = TtkScrollbar(self)
        scrollbar.pack(side="right", fill="y")

        self.listbox = Listbox(
            self,
            yscrollcommand=scrollbar.set,
            height=height,
            width=width,
            font=("Courier", 10),
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.listbox.yview)

        # Bind selection
        self.listbox.bind("<<ListboxSelect>>", self._on_select)
        logger.debug("DeviceListWidget intitialized")

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
        index = selection[0]
        line = self.listbox.get(index)
        # Parse device name from formatted line
        # Format: "router | 192.168.0.1:80 | 🟢"
        if " | " in line:
            parts = line.split(" | ")
            name_part = parts[0].strip()
            return name_part
        return None

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
        status_icons = {
            "online": "🟢",
            "offline": "🔴",
            "unknown": "⚪"
        }
        status_key = (
            "online"
            if device.is_online
            else "offline"
            if device.is_online is False
            else "unknown"
        )
        icon = status_icons.get(status_key)
        return f"{device.name} | {device.ip_address}:{device.port} | {icon} ({status_key})"
    
    def _on_select(self, event) -> None:
        """Handle list selection event."""
        selection = self.listbox.curselection()
        if selection:
            self.selected_index = selection[0]
            logger.debug(f"Device selected at index {self.selected_index}")
