# src/controllers/__init__.py
"""
Controllers package.

Handles backend logic subscribing/publishing events to the bus.
"""
from src.controllers.main import MainController

__all__ = ["MainController"]
