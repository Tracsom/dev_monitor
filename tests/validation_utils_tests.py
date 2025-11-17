# tests/validation_utils_tests.py
"""
Tests for validation utilities.
"""
import pytest
from src.utils.validators import DeviceValidator
from src.exceptions import ValidationError


class TestDeviceValidator:
    """Test device validator."""

    def test_valid_device_name(self):
        """Test valid device names."""
        assert DeviceValidator.validate_device_name("router-1") == "router-1"
        assert (
            DeviceValidator.validate_device_name("server_prod.01")
            == "server_prod.01"
        )

    def test_invalid_device_name(self):
        """Test invalid device names."""
        with pytest.raises(ValidationError):
            DeviceValidator.validate_device_name("")

        with pytest.raises(ValidationError):
            DeviceValidator.validate_device_name("a" * 51)

    def test_valid_ip(self):
        """Test valid IP addresses."""
        assert (
            DeviceValidator.validate_ip_address("192.168.1.1") == "192.168.1.1"
        )

    def test_invalid_ip(self):
        """Test invalid IP addresses."""
        with pytest.raises(ValidationError):
            DeviceValidator.validate_ip_address("256.1.1.1")

        with pytest.raises(ValidationError):
            DeviceValidator.validate_ip_address("invalid")

    def test_valid_port(self):
        """Test valid ports."""
        assert DeviceValidator.validate_port(80) == 80
        assert DeviceValidator.validate_port(65535) == 65535

    def test_invalid_port(self):
        """Test invalid ports."""
        with pytest.raises(ValidationError):
            DeviceValidator.validate_port(0)

        with pytest.raises(ValidationError):
            DeviceValidator.validate_port(65536)
