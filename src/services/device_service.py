# src/services/device_service.py
"""
Service for managing devices and their status checks.
"""
import logging
import socket
import subprocess
import platform
from typing import List, Optional
from src.models import Device, DeviceRepository
from src.config import Config
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

    def add_device(
        self, name: str, ip_address: str, port: int = 80, timeout: int = 5
    ) -> bool:
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
                name=name, ip_address=ip_address, port=port, timeout=timeout
            )

            # Check for duplicate names
            if any(d.name == name for d in self.devices):
                logger.warning(
                    f"Device with name {name!r} already exists"
                )
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
        Check if a device is online using:
          1) TCP connect to device.port
          2) TCP connect to fallback ports from Config.FALLBACK_PORTS
          3) ICMP ping (system 'ping') as last resort

        Updates device.is_online, device.last_checked and persists via repository.
        """
        def tcp_probe(host: str, port: int, timeout: int) -> bool:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(timeout)
                    return sock.connect_ex((host, port)) == 0
            except Exception as e:
                logger.debug("tcp_probe error for %s:%s -> %s", host, port, e)
                return False
            
        def ping_probe(host: str, timeout: str) -> bool:
            """
            Use system ping as a last resort.
            - Linux/macOS: ping -c 1 -W timeout
            - Windows: ping -n 1 -w timeout_ms
            """
            try:
                system = platform.system().lower()
                if system == "windows":
                    cmd = ["ping", "-n", "1", "-w", str(int(timeout * 1000)), host]
                else:
                    # use -c 1 (one packet) and -W for timeout (seconds)
                    cmd = ["ping", "-c", "1", "-w", str(int(timeout)), host]
                proc = subprocess.run(
                    cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                return proc.returncode == 0
            except Exception as e:
                logger.debug("ping_probe error for %s -> %s", host, e)
                return False

        try:
            host = device.ip_address
            timeout = max(1, device.timeout or Config.DEFAULT_TIMEOUT)

            # 1) Try the device's configured port first
            logger.debug("Checking %s on configured port: %s", device.name, device.port)
            if tcp_probe(host, device.port, timeout):
                device.is_online = True
                device.last_checked = datetime.now().isoformat()
                self.repository.update_device(device)
                logger.info("Device %s is online (port %s)", device.name, device.port)
                return True
            
            for p in Config.FALLBACK_PORTS:
                if p == device.port:
                    continue
                logger.debug("Trying fallback port %s for %s", p, device.name)
                if tcp_probe(host, p, timeout):
                    device.is_online = True
                    device.last_checked = datetime.now().isoformat()
                    self.repository.update_device(device)
                    logger.info(
                        "Device %s is online (fallback port %s)", device.name, p
                    )
                    return True
                
            # 3) Final fallback: ICMP ping
            logger.debug("Trying ping fallback %s", device.name)
            if ping_probe(host, str(Config.PING_TIMEOUT)):
                device.is_online = True
                device.last_checked = datetime.now().isoformat()
                self.repository.update_device(device)
                logger.info("Device %s is reachable via ICMP ping", device.name)
                return True
            
            # All probes failed
            device.is_online = False
            device.last_checked = datetime.now().isoformat()
            self.repository.update_device(device)
            logger.info("Device %s appears offline (all probes failed)", device.name)
            return False
        
        except Exception as e:
            logger.exception("Error checking device %s:%s", device.name, e)
            device.is_online = False
            device.last_checked = datetime.now().isoformat()
            try:
                self.repository.update_device(device)
            except Exception as e:
                logger.exception("Failed to persist device status for %s", device.name)
            return False

    def check_all_devices(self) -> None:
        """Check status of all enabled devices."""
        enabled_devices = [d for d in self.devices if d.enabled]
        logger.info(
            f"Checking status of {len(enabled_devices)} enabled devices"
        )

        # run checks in a threaded pool to improve responsiveness for many devices
        max_workers = min(32, max(2, len(enabled_devices)))
        with ThreadPoolExecutor(max_workers=max_workers) as ex:
            futures = {
                ex.submit(self.check_device_status, d): d
                for d in enabled_devices
            }
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
