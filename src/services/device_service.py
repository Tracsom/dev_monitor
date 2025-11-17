# src/services/device_service.py
"""
Service for managing devices and their status checks.
"""
import logging
import socket
from typing import List, Optional
from src.models import Device, DeviceRepository
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class DeviceService:
    """Service for managing devices and checking their status."""

    def __init__(self, repository: Optional[DeviceRepository] = None):
        """
        Initialize the device service.

        Args:
            repository: DeviceRepository instance (uses default if not provided)
        """
        self.repository = repository or DeviceRepository()
        self.devices: List[Device] = []
        self._load_devices()

    def _load_devices(self):
        """Load devices from repository."""
        self.devices = self.repository.load_all()
        logger.info(f"Device service loaded {len(self.devices)} devices")

    def get_all_devices(self) -> List[Device]:
        """
        Get all managed devices.

        Returns:
            List of Device objects
        """
        return self.devices.copy()
    
    def add_device(self, name: str, ip_address: str, port: int = 80, timeout: int = 5) -> bool:
        """
        Add a new device.

        Args:
            name: Device name
            ip_address: Device IP address
            port: Device port (Default 80)
            timeout: Connection timeout in seconds (default 5)

        Return:
            True if device was added successfully, False otherwise
        """
        try:
            device = Device(
                name=name,
                ip_address=ip_address,
                port=port,
                timeout=timeout
            )

            # Check for duplicate names
            if any(d.name == name for d in self.devices):
                logger.warning(f"Device with name {name!r} already exists")
                return False
            
            self.devices.append(device)
            success = self.repository.add_device(device)

            if success:
                logger.info(f"Added device: {name} ({ip_address}:{port})")

            return success
        except ValueError as e:
            logger.error(f"Invalid device data: {e}")
            return False
        except Exception as e:
            logger.error(f"Error adding device: {e}", exc_info=True)
            return False
        
    def remove_device(self, device_name: str) -> bool:
        """
        Remove a device.

        Args:
            device_name: Name of device to remove

        Returns:
            True if device was removed, False otherwise
        """
        self.devices = [d for d in self.devices if d.name != device_name]
        success = self.repository.remove_device(device_name)

        if success:
            logger.info(f"Removed device: {device_name}")

        return success
    
    def check_device_status(self, device: Device) -> bool:
        """
        Check if a device is online by attempting a TCP connection.

        Args:
            device: Device to check

        Returns:
            True if device is online, False otherwise
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(device.timeout)
            result = sock.connect_ex((device.ip_address, device.port))
            sock.close()

            is_online = result == 0
            device.is_online = is_online
            device.last_checked = datetime.now().isoformat()

            # Update in repository
            self.repository.update_device(device)

            status_str = "online" if is_online else "offline"
            logger.debug(f"Device {device.name} is {status_str}")

            return is_online
        
        except socket.gaierror as e:
            logger.error(f"DNS resolution failed for {device.ip_address}: {e}")
            device.is_online = False
            device.last_checked = datetime.now().isoformat()
            return False
        
        except socket.timeout:
            logger.debug(f"Connection timeout for {device.name} ({device.ip_address}:{device.port})")
            device.is_online = False
            device.last_checked = datetime.now().isoformat()
            return False
        
        except Exception as e:
            logger.error(f"Error checking device {device.name}: {e}", exc_info=True)
            device.is_online = False
            return False
        
    def check_all_devices(self) -> None:
        """Check status of all enabled devices."""
        enabled_devices = [d for d in self.devices if d.enabled]
        logger.info(f"Checking status of {len(enabled_devices)} enabled devices")

        # run checks in a threaded pool to improve responsiveness for many devices
        with ThreadPoolExecutor(max_workers=min(32, max(2, len(enabled_devices)))) as ex:
            futures = {ex.submit(self.check_device_status, d): d for d in enabled_devices}
            for fut in as_completed(futures):
                try:
                    fut.result()
                except Exception as e:
                    logger.exception("Exception during device check: %s", e)

    def enable_device(self, device_name: str) -> bool:
        """
        Enable a device for monitoring.

        Args:
            device_name: Name of device to enable

        Returns:
            True if successful, False otherwise
        """
        for device in self.devices:
            if device.name == device_name:
                device.enabled = True
                return self.repository.update_device(device)
            
        return False
    
    def disable_device(self, device_name: str) -> bool:
        """
        Disable a device from monitoring.

        Args:
            device_name: Name of device to disable

        Returns:
            True if successful, False otherwise
        """
        for device in self.devices:
            if device.name == device_name:
                device.enabled = False
                return self.repository.update_device(device)
            
        return False