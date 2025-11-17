# src/ui/dialog_manager.py
"""
Dialog utilities for user input and feedback.
"""
import logging
from tkinter import simpledialog, messagebox
from tkinter import Tk
from typing import Optional, Tuple

logger = logging.getLogger(__name__)

class DialogManager:
    """Manages all dialog interactions."""

    @staticmethod
    def ask_device_details(parent: Tk) -> Optional[Tuple[str, str, int, int]]:
        """
        Prompt user for device details.

        Args:
            parent: Parent window

        Returns:
            Tuple of (name, ip, port, timeout) or None if cancelled
        """
        name = simpledialog.askstring("Device Name", "Enter device name", parent=parent)
        if not name:
            return None
        
        ip = simpledialog.askstring("IP address", "Enter device IP address:", parent=parent)
        if not ip:
            return None
        
        port = simpledialog.askinteger(
            "Port",
            "Enter a port (1-65535):",
            parent=parent,
            initialvalue=80,
            minvalue=1,
            maxvalue=65535
        )
        if port is None:
            return None
        
        timeout = simpledialog.askinteger(
            "Timeout",
            "Enter timeout seconds:", 
            parent=parent,
            initialvalue=5,
            minvalue=1
        )
        if timeout is None:
            return None
        
        return (name, ip, port, timeout)
    
    @staticmethod
    def confirm_remove(parent: Tk, device_name: str) -> bool:
        """
        Confirm device removal.

        Args:
            parent: Parent window
            device_name: Name of device to remove

        Returns:
            True if user confirmed, False otherwise
        """
        return messagebox.askyesno(
            "Confirm remove",
            f"Remove device: {device_name}?",
            parent=parent
        )
    
    @staticmethod
    def show_success(parent: Tk, title: str, message: str) -> None:
        """
        Show success message.

        Args:
            parent: Parent window
            title: Dialog title
            message: Message text
        """
        messagebox.showinfo(title, message, parent=parent)

    @staticmethod
    def show_error(parent: Tk, title: str, message: str) -> None:
        """
        Show error message.

        Args:
            parent: Parent window
            title: Dialog title
            message: Message text
        """
        messagebox.showerror(title, message, parent=parent)

    @staticmethod
    def show_warning(parent: Tk, title: str, message: str) -> None:
        """
        Show warning message.

        Args:
            parent: Parent window
            title: Dialog title
            message: Message text
        """
        messagebox.showwarning(title, message, parent=parent)