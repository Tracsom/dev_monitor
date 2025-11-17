# src/exceptions.py
"""
Custom application exceptions.
"""


class DevMonitorException(Exception):
    """Base exception for Dev Monitor."""

    pass


class DeviceError(DevMonitorException):
    """Raised for device-related errors."""

    pass


class DeviceNotFoundError(DeviceError):
    """Raised when a device is not found."""

    pass


class DuplicateDeviceError(DeviceError):
    """Raised when attempting to add a duplicate device."""

    pass


class RepositoryError(DevMonitorException):
    """Raised for repository/persistence errors."""

    pass


class ValidationError(DevMonitorException):
    """Raised for validation errors."""

    pass


class NetworkError(DevMonitorException):
    """Raised for network-related errors."""

    pass
