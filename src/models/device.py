# src/models/device.py
"""
Device model for representing monitored IP devices.
"""
from dataclasses import dataclass, asdict
from typing import Optional
from datetime import datetime
from src.utils.validators import DeviceValidator


@dataclass
class Device:
    """Represents a remote IP device to be monitored."""

    name: str
    ip_address: str
    port: int = 80
    timeout: int = 5
    enabled: bool = True
    created_at: Optional[str] = None
    last_checked: Optional[str] = None
    is_online: Optional[bool] = None

    def __post_init__(self):
        """Validate device data and set creation timestamp."""
        self.name = DeviceValidator.validate_device_name(self.name)
        self.ip_address = DeviceValidator.validate_ip_address(self.ip_address)
        self.port = DeviceValidator.validate_port(self.port)
        self.timeout = DeviceValidator.validate_timeout(self.timeout)

        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> dict:
        """Convert the device to a dictionary for serialization."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Device":
        """Create a Device instance from a dictionary."""
        return cls(**data)

    def __repr__(self) -> str:
        status = (
            "Online"
            if self.is_online
            else "Offline"
            if self.is_online is False
            else "Unknown"
        )
        return (
            f"Device (name={self.name}, ip_address={self.ip_address}, "
            f"status={status})"
        )
