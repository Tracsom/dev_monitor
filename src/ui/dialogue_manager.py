# src/ui/dialog_manager.py
"""
Dialog utilities for user input and feedback.
"""
import logging
from tkinter import simpledialog, messagebox
from tkinter import Tk, StringVar
from typing import Optional, Tuple, Callable

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
        name = simpledialog.askstring(
            "Device Name", "Enter device name", parent=parent
        )
        if not name:
            return None

        ip = simpledialog.askstring(
            "IP address", "Enter device IP address:", parent=parent
        )
        if not ip:
            return None

        port = simpledialog.askinteger(
            "Port",
            "Enter a port (1-65535):",
            parent=parent,
            initialvalue=80,
            minvalue=1,
            maxvalue=65535,
        )
        if port is None:
            return None

        timeout = simpledialog.askinteger(
            "Timeout",
            "Enter timeout seconds:",
            parent=parent,
            initialvalue=5,
            minvalue=1,
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
            "Confirm remove", f"Remove device: {device_name}?", parent=parent
        )

    @staticmethod
    def show_success(
        title: str, 
        message: str, 
        status_var: Optional[StringVar] = None,
        parent: Optional[Tk] = None,
        modal: bool = False,
    ) -> None:
        """
        Shows success message.

        Args:
            title: Dialog title
            message: Message text
            status_var: Optional StringVar to update status bar
            parent: Optional parent window (required if modal=True)
            modal: If True, show modal dialog; else update status bar
        """
        if modal and parent:
            messagebox.showinfo(title, message, parent=parent)
        elif status_var:
            status_var.set(f"✓ {message}")
            logger.debug(f"Status: {message}")
        else:
            logger.info(f"{title}: {message}")

    @staticmethod
    def show_error(
        title: str, 
        message: str, 
        status_var: Optional[StringVar] = None,
        parent: Optional[Tk] = None,
        modal: bool = False,
    ) -> None:
        """
        Show error message.

        Args:
            title: Dialog title
            message: Message text
            status_var: Optional StringVar to update status bar
            parent: Optional parent window (required if modal=True)
            modal: If True, show modal dialog; else update status bar
        """
        if modal and parent:
            messagebox.showerror(title, message, parent=parent)
        elif status_var:
            status_var.set(f"x Error: {message}")
            logger.error(f"{title}: {message}")
        else:
            logger.error(f"{title}: {message}")

    @staticmethod
    def show_warning(
        title: str, 
        message: str, 
        status_var: Optional[StringVar] = None,
        parent: Optional[Tk] = None,
        modal: bool = False,
    ) -> None:
        """
        Show warning message.

        Args:
            title: Dialog title
            message: Message text
            status_var: Optional StringVar to update status bar
            parent: Optional parent window (required if modal=True)
            modal: If True, show modal dialog; else update status bar
        """
        if modal and parent:
            messagebox.showwarning(title, message, parent=parent)
        elif status_var:
            status_var.set(f"⚠ Warning: {message}")
            logger.warning(f"{title}: {message}")
        else:
            logger.warning(f"{title}: {message}")