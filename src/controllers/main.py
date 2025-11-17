# src/controllers/main.py
"""
Main controller for the application.
"""
import logging
from typing import Optional, List
from src.bus import Scheduler
from src.services import DeviceService
from src.models import Device

logger = logging.getLogger(__name__)


class MainController:
    """Main application controller."""

    def __init__(self, scheduler: Optional[Scheduler] = None):
        """
        Initialize the main controller.

        Args:
            scheduler: Event bus for publishing/subscribing to events
        """
        self.scheduler = scheduler or Scheduler()
        self.device_service = DeviceService()
        self._setup_event_handlers()
        logger.info("MainController initialized")

    def _setup_event_handlers(self) -> None:
        """Set up event handlers for the controller."""
        if self.scheduler:
            self.scheduler.subscribe("add_device", self.handle_add_device)
            self.scheduler.subscribe(
                "remove_device", self.handle_remove_device
            )
            self.scheduler.subscribe(
                "check_all_devices", self.handle_check_all_devices
            )
            self.scheduler.subscribe("get_devices", self.handle_get_devices)
            logger.debug("Event handlers registered")

    def handle_add_device(
        self, name: str, ip_address: str, port: int = 80, timeout: int = 5
    ) -> bool:
        """
        Handle add device event.

        Args:
            name: Device name
            ip_address: Device IP address
            port: Device port
            timeout: Connection timeout

        Returns:
            True if decvice was added successfully
        """
        result = self.device_service.add_device(
            name, ip_address, port, timeout
        )
        self.scheduler.publish(
            "device_added" if result else "device_add_failed", name
        )
        return result

    def handle_remove_device(self, device_name: str) -> bool:
        """
        Handle remove device event.

        Args:
            device_name: Name of device to remove

        Returns:
            True if device was remove successfully
        """
        result = self.device_service.remove_device(device_name)
        self.scheduler.publish(
            "device_removed" if result else "device_remove_failed", device_name
        )
        return result

    def handle_check_all_devices(self) -> None:
        """Handle check all devices event."""
        self.device_service.check_all_devices()
        devices = self.device_service.get_all_devices()
        self.scheduler.publish("devices_checked", devices)

    def handle_get_devices(self) -> List[Device]:
        """
        Handles get devices event.

        Returns:
            List of all devices
        """
        return self.device_service.get_all_devices()

    def __repr__(self) -> str:
        return (
            f"MainController(scheduler={self.scheduler!r}, "
            f"devices={len(self.device_service.devices)})"
        )
