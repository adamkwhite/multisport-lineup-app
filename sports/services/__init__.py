"""
Sports services module.

Provides factory functions and configuration loaders for lineup generation.
"""

from sports.services.lineup_factory import (
    get_lineup_generator,
    get_supported_sports,
    is_sport_supported,
)
from sports.services.sport_loader import load_sport_config

__all__ = [
    "get_lineup_generator",
    "get_supported_sports",
    "is_sport_supported",
    "load_sport_config",
]
