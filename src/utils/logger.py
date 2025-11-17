# src/utils/logger.py
"""
Logging configuration and utilities.
"""
import logging
import logging.handlers
from pathlib import Path
from src.config import Config

def setup_logging(debug: bool = False) -> None:
    """
    Configure application logging.

    Args:
        debug: Enable debug level logging
    """
    # Ensure log directory exists
    Config.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Set level
    level = logging.DEBUG if debug else getattr(logging, Config.LOG_LEVEL, logging.INFO)

    # Set formatter
    formatter = logging.Formatter(Config.LOG_FORMAT)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers
    root_logger.handlers.clear()

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=Config.LOG_MAX_BYTES,
        backupCount=Config.LOG_BACKUP_COUNT
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    logging.info(f"Logging initialized at level {logging.getLevelName(level)}")