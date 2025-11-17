# src/utils/validators.py
"""
Input validation utilities.
"""
import re
from src.exceptions import ValidationError


class DeviceValidator:
    """Validates device input data."""

    DEVICE_NAME_PATTERN = r"^[a-zA-Z0-9_\-\.]{1,50}$"
    IP_PATTERN = r"^(\d{1,3}\.){3}\d{1,3}$"

    @staticmethod
    def validate_device_name(name: str) -> str:
        """
        Validate device name.

        Args:
            name: Device name

        Returns:
            Validated name

        Raises:
            ValidationError: If name is invalid
        """
        if not name or not name.strip():
            raise ValidationError("Device name cannot be empty")

        name = name.strip()
        if len(name) > 50:
            raise ValidationError("Device name cannot exceed 50 characters")

        if not re.match(DeviceValidator.DEVICE_NAME_PATTERN, name):
            raise ValidationError(
                "Device name contains invalid characters"
            )

        return name

    @staticmethod
    def validate_ip_address(ip: str) -> str:
        """
        Validate IP address format.

        Args:
            ip: IP address string

        Returns:
            Validated IP

        Raises:
            ValidationError: If IP is invalid
        """
        if not ip or not ip.strip():
            raise ValidationError("IP address cannot be empty")

        ip = ip.strip()
        if not re.match(DeviceValidator.IP_PATTERN, ip):
            raise ValidationError(f"Invalid IP address format: {ip}")

        # Validate octects
        octets = [int(x) for x in ip.split(".")]
        if not all(0 <= octect <= 255 for octect in octets):
            raise ValidationError("IP octets must be between 0 and 255")

        return ip

    @staticmethod
    def validate_port(port: int) -> int:
        """
        Validate port number.

        Args:
            port: Port number

        Returns:
            Validated port

        Raises:
            ValidationError: If port is invalid
        """
        if not isinstance(port, int):
            raise ValidationError(f"Port must be an integer, got {type(port)}")

        if not (1 <= port <= 65535):
            raise ValidationError(
                f"Port must be between 1 and 65535, got {port}"
            )

        return port

    @staticmethod
    def validate_timeout(timeout: int) -> int:
        """
        Validate timeout value.

        Args:
            timeout: Timeout in seconds

        Returns:
            Validated timeout

        Raises:
            ValidationError: If timeout invalid
        """
        if not isinstance(timeout, int):
            raise ValidationError(
                f"Timeout must be an integer, got {type(timeout)}"
            )

        if timeout < 1:
            raise ValidationError(
                f"Timeout must be at least 1 second, got {timeout}"
            )

        if timeout > 300:
            raise ValidationError(
                f"Timeout cannot exceed 300 seconds, got {timeout}"
            )

        return timeout
