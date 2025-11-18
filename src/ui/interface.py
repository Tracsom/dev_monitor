# src/ui/interface.py
"""
Main UI interface using tkinter
"""
import logging
from tkinter import Tk, StringVar
from tkinter.ttk import (
    Frame as TtkFrame,
    Button as TtkButton,
    Label as TtkLabel,
)
from typing import Optional, List, Callable
from src.bus import Scheduler
from src.models import Device
from src.ui.device_list_widget import DeviceListWidget
from src.ui.ui_event_handlers import UIEventHandlers
from src.ui.ui_commands import UICommands
from src.ui.progress_manager import ProgressManager

logger = logging.getLogger(__name__)


class Interface:
    """Main user interface class (using Tkinter)."""

    def __init__(
        self,
        scheduler: Optional[Scheduler] = None,
        shutdown_callback: Optional[Callable[[], None]] = None,
    ):
        """
        Initialize the interface.

        Args:
            scheduler: Event bus for publishing/subscribing to events
            shutdown_callback: Optional callback for graceful shutdown
        """
        self.scheduler = scheduler or Scheduler()
        self.shutdown_callback = shutdown_callback
        self.root: Optional[Tk] = None
        self.device_list_widget: Optional[DeviceListWidget] = None
        self.commands: Optional[UICommands] = None
        self.event_handlers: Optional[UIEventHandlers] = None
        self.status_var: Optional[StringVar] = None
        self.progress_manager: Optional[ProgressManager] = None
        # Store button references for enable/disable
        self._action_buttons: List[TtkButton] = []

        logger.info("Interface initialized")

    def launch(self, debug: bool = False) -> None:
        """
        Launch the UI.

        Args:
            debug: Enable debug mode
        """
        if debug:
            logger.debug("Launching UI in debug mode")
        else:
            logger.info("Launching UI")

        self.root = Tk()
        self.root.title("Dev Monitor")
        # bind close to allow graceful shutdown of background services
        if self.shutdown_callback:

            def _on_close():
                try:
                    self.shutdown_callback()
                finally:
                    self.root.destroy()

            self.root.protocol("WM_DELETE_WINDOW", _on_close)
        self._build_ui()
        self._setup_event_handlers()
        self._refresh_devices()
        self.root.mainloop()

    def _build_ui(self) -> None:
        """Build the Tkinter UI."""
        # `launch()` sets `self.root` before calling this method; assert so mypy knows it's not None
        assert self.root is not None

        frame = TtkFrame(self.root, padding=8)
        frame.grid(row=0, column=0, sticky="nsew")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        # Device list
        self.device_list_widget = DeviceListWidget(frame, height=12, width=60)
        self.device_list_widget.grid(
            row=0, column=0, sticky="ew", padx=(8, 0), pady=(8, 0),
        )

        # Progress manager (initially hidden)
        self.progress_manager = ProgressManager(frame)

        # Buttons
        add_btn = TtkButton(
            frame, text="Add Device", command=self._on_add_device
        )
        add_btn.grid(row=1, column=0, sticky="ew", pady=(8, 0))
        self._action_buttons.append(add_btn)

        remove_btn = TtkButton(
            frame, text="Remove Selected", command=self._on_remove_selected
        )
        remove_btn.grid(row=1, column=1, sticky="ew", padx=(8, 0), pady=(8, 0))
        self._action_buttons.append(remove_btn)

        check_btn = TtkButton(
            frame, text="Check All", command=self._on_check_all
        )
        check_btn.grid(row=1, column=2, sticky="ew", padx=(8, 0), pady=(8, 0))
        self._action_buttons.append(check_btn)

        refresh_btn = TtkButton(
            frame, text="Refresh", command=self._on_refresh
        )
        refresh_btn.grid(row=1, column=3, sticky="ew", padx=(8, 0), pady=(8, 0))
        self._action_buttons.append(refresh_btn)

        # Status label
        self.status_var = StringVar(value="Ready")
        status_label = TtkLabel(frame, textvariable=self.status_var)
        status_label.grid(
            row=2, column=0, columnspan=4, sticky="w", pady=(8, 0)
        )

        # Layout configuration
        frame.rowconfigure(0, weight=1)
        for c in range(4):
            frame.columnconfigure(c, weight=1)

        # Bind double-click
        self.device_list_widget.bind_double_click(self._on_check_all)

    def _setup_event_handlers(self) -> None:
        """Set up event handlers and commands."""
        # root and status_var will be set by `_build_ui`; assert to satisfy type checker
        assert self.root is not None
        assert self.status_var is not None
        assert self.progress_manager is not None

        self.commands = UICommands(
            self.scheduler, 
            self.root, 
            self.status_var, 
            self._refresh_devices,
            progress_manager=self.progress_manager,
            disable_buttons_callback=self._disable_action_buttons,
        )
        self.event_handlers = UIEventHandlers(
            self.scheduler, 
            self.root, 
            self._refresh_devices,
            self.status_var
        )

    def _disable_action_buttons(self, disable: bool) -> None:
        """
        Disable or enable action buttons.

        Args:
            disable: True to disable, False to enable
        """
        state = "disabled" if disable else "normal"
        for btn in self._action_buttons:
            btn.config(state=state)
        logger.debug("Action buttons %s", state)

    def _refresh_devices(self) -> None:
        """Refresh the device list from controller."""
        assert self.status_var is not None
        results = self.scheduler.publish("get_devices")
        devices: List[Device] = []
        if results and isinstance(results[0], list):
            devices = results[0]

        if self.device_list_widget:
            self.device_list_widget.populate(devices)

        self.status_var.set(f"Loaded {len(devices)} devices")
        logger.debug(f"Refreshed UI with {len(devices)} devices")

    def _on_add_device(self) -> None:
        """Handle add device button."""
        assert self.commands is not None
        self.commands.add_device()

    def _on_remove_selected(self) -> None:
        """Handle remove device button."""
        assert self.device_list_widget is not None
        assert self.commands is not None
        get_name = self.device_list_widget.get_selected_device_name
        self.commands.remove_device(get_name)

    def _on_check_all(self) -> None:
        """Handle check all button."""
        assert self.commands is not None
        self.commands.check_all()

    def _on_refresh(self) -> None:
        """Handle refresh button."""
        assert self.commands is not None
        self.commands.refresh()

    def __repr__(self) -> str:
        return f"Interface(scheduler={self.scheduler!r})"
