# src/ui/progress_manager.py
import logging
from tkinter.ttk import Progressbar, Label
from tkinter import Frame
from typing import Optional

logger = logging.getLogger(__name__)

class ProgressManager:
    """Manages progress bar and operation feedback."""

    def __init__(self, parent):
        """
        Initialize progress manager.

        Args:
            parent: Parent frame to attach progress bar to
        """
        self.parent = parent
        self.progress_bar = Progressbar(parent, mode="indeterminate")
        self.status_label = Label(parent, text="")
        self.visible = False

    def show(self, message: str = "Processing...") -> None:
        """
        Show progress bar with message.

        Args:
            message: Status message to display
        """
        if not self.visible:
            self.status_label.config(text=message)
            self.status_label.grid(
                row=3, column=0, columnspan=4, sticky="ew", pady=(8, 0)
            )
            self.progress_bar.grid(
                row=4, column=0, columnspan=4, sticky="ew", pady=(4, 0)
            )
            self.progress_bar.start()
            self.visible = True
            logger.debug("Progress bar shown: %s", message)

    def hide(self) -> None:
        """Hide progress bar and status."""
        if self.visible:
            self.progress_bar.stop()
            self.progress_bar.grid_remove()
            self.status_label.grid_remove()
            self.visible = False
            logger.debug("Progress bar hidden")

    def update_message(self, message: str) -> None:
        """
        Update status message while visible.

        Args:
            message: New status message
        """
        self.status_label.config(text=message)
        logger.debug("Progress message updated: %s", message)