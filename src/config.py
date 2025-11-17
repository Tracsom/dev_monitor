# src/utils/config.py
"""
Application configuration managment.
"""
import os
from pathlib import Path


class Config:
    """Application configuration."""

    # Paths
    APP_NAME = "Dev Monitor"
    APP_DIR = Path.home() / ".dev_monitor"
    DEVICES_FILE = APP_DIR / "devices.json"
    LOG_FILE = APP_DIR / "app.log"

    # Defaults
    DEFAULT_PORT = 80
    DEFAULT_TIMEOUT = 5
    DEFAULT_CHECK_INTERVAL = 300  # 5 minutes

    # Fallback/network probes
    # Order of ports to try after device.port (don't duplicate device.port)
    FALLBACK_PORTS = [443, 80, 22, 8080]
    # Ping timeout in seconds (used for system ping fallback)
    PING_TIMEOUT = 2

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "[%(asctime)s] %(levelname)-8s %(name)s: %(message)s"
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5

    # UI
    WINDOW_HEIGHT = 800
    WINDOW_WIDTH = 600

    # Features
    AUTO_CHECK_ENABLED = True
    SHOW_TIMESTAMPS = True
