# src/models/__init__.py
"""
Models package.

Contains data models for the application.
"""
from src.models.device import Device
from src.models.device_repository import DeviceRepository

__all__ = ["Device", "DeviceRepository"]
