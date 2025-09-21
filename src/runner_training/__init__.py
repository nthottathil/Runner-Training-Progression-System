"""Runner Training System - A comprehensive training progression calculator."""

__version__ = "1.2.0"
__author__ = "Neha Thottathil"

from .models.factory import ModelFactory
from .config.settings import Settings

__all__ = ["ModelFactory", "Settings"]