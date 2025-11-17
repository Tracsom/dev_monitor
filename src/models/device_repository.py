# src/models/device_repository.py
"""
Repository for persisting devices to JSON storage.
"""
import json
import logging
import os
from pathlib import Path
from typing import List, Optional
from src.models.device import Device
from src.config import Config
import threading

logger = logging.getLogger(__name__)

class DeviceRepository:
    """Handles persistence of devices to JSON file storage."""

    DEFAULT_STORAGE_PATH = Config.DEVICES_FILE

    def __init__(self, storage_path: Optional[Path] = None):
        """
        Initialize repository.

        Args:
            storage_path: Path to JSON storage file. defaults to ~/.dev_monitor/devices.json
        """
        self.storage_path = storage_path or self.DEFAULT_STORAGE_PATH
        self._lock = threading.Lock()
        self._ensure_storage_directory()
        logger.info(f"DeviceRepository initialized with storage path: {self.storage_path}")

    def _ensure_storage_directory(self):
        """Create storage directory if it doesn't exist."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

    def load_all(self) -> List[Device]:
        """
        Load all devices from storage.
        """
        with self._lock:
            if not self.storage_path.exists():
                logger.info(f"No devices file found at {self.storage_path}, return empty list")
                return []
            
            try:
                with open(self.storage_path, 'r', encoding="utf-8") as f:
                    data = json.load(f)

                devices = [Device.from_dict(device_data) for device_data in data]
                logger.info(f"Loaded {len(devices)} devices from storage")
                return devices
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding JSON from {self.storage_path}: {e}", exc_info=True)
                return []
            except Exception as e:
                logger.error(f"Error loading devices: {e}", exc_info=True)
                return []
        
    def save_all(self, devices: List[Device]) -> bool:
        """
        Save all devices to storage.
        
        Args:
            devices: List of Device objects to save

        Returns:
            True if successful, False otherwise
        """
        data = [device.to_dict() for device in devices]
        tmp_path = self.storage_path.with_suffix(".tmp")
        try:
            with self._lock:
                with open(tmp_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=2)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp_path, self.storage_path)
            logger.info(f"Saved {len(devices)} devices to storage")
            return True
        except Exception as e:
            logger.error(f"Error saving devices: {e}", exc_info=True)
            # cleanup tmp file if exists
            try:
                if tmp_path.exists():
                    tmp_path.unlink()
            except Exception:
                pass
            return False
        
    def add_device(self, device: Device) -> bool:
        """
        Add a single device to storage.

        Args:
            device: Device object to add

        Returns:
            True if successful, False otherwise
        """
        devices = self.load_all()
        devices.append(device)
        return self.save_all(devices)
    
    def remove_device(self, device_name: str) -> bool:
        """
        Remove a device by name.

        Args:
            device_name: Name of a device to remove

        Returns:
            True if device was found and removed, False otherwise
        """
        devices = self.load_all()
        original_count = len(devices)
        devices = [d for d in devices if d.name != device_name]

        if len(devices) < original_count:
            self.save_all(devices)
            logger.info(f"Removed device: {device_name}")
            return True

        logger.warning(f"Device not found: {device_name}")
        return False

    def update_device(self, device: Device) -> bool:
        """
        Update an existing device.

        Args:
            device: Updated Device object

        Returns:
            True if device was found and updated, False otherwise
        """
        devices = self.load_all()

        for i, d in enumerate(devices):
            if d.name == device.name:
                devices[i] = device
                self.save_all(devices)
                logger.info(f"Updated device: {device.name}")
                return True

        logger.warning(f"Device not found for update: {device.name}")
        return False
    
    def get_device(self, device_name: str) -> Optional[Device]:
        """
        Get a device by name.

        Args:
            device_name: Name of device to retrieve

        Returns:
            Device object if found, None otherwise
        """
        devices = self.load_all()
        for device in devices:
            if device.name == device_name:
                return device
        return None