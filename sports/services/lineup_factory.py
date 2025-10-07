"""
Factory for creating sport-specific lineup generators.

This module provides a factory function that returns the appropriate
LineupGenerator instance based on the sport ID.
"""

from typing import Optional

from sports.generators.base import LineupGenerator
from sports.generators.baseball import BaseballLineupGenerator
from sports.generators.volleyball import VolleyballLineupGenerator
from sports.services.sport_loader import load_sport_config


def get_lineup_generator(sport_id: str) -> LineupGenerator:
    """
    Factory function to create the appropriate lineup generator for a sport.

    This factory provides runtime sport selection by returning the correct
    generator instance based on the sport ID. Each generator is initialized
    with its corresponding sport configuration.

    Args:
        sport_id: Sport identifier ("baseball", "soccer", "volleyball")

    Returns:
        LineupGenerator instance for the specified sport

    Raises:
        ValueError: If sport_id is not recognized or supported

    Example:
        >>> generator = get_lineup_generator("baseball")
        >>> lineups = generator.generate(players, game_info)
    """
    # Validate sport_id
    if not sport_id:
        raise ValueError("sport_id is required")

    if not isinstance(sport_id, str):
        raise ValueError(f"sport_id must be a string, got {type(sport_id).__name__}")

    # Normalize to lowercase for case-insensitive matching
    sport_id = sport_id.lower().strip()

    # Load sport configuration
    try:
        config = load_sport_config(sport_id)
    except FileNotFoundError:
        raise ValueError(
            f"Unknown sport: '{sport_id}'. "
            f"Supported sports: baseball, soccer, volleyball"
        )

    # Return appropriate generator based on sport
    if sport_id == "baseball":
        return BaseballLineupGenerator(config)
    elif sport_id == "soccer":
        # TODO: Implement SoccerLineupGenerator
        raise NotImplementedError(
            "Soccer lineup generation is not yet implemented."
        )
    elif sport_id == "volleyball":
        return VolleyballLineupGenerator(config)
    else:
        raise ValueError(
            f"Unknown sport: '{sport_id}'. "
            f"Supported sports: baseball, soccer, volleyball"
        )


def get_supported_sports() -> list[str]:
    """
    Get list of currently supported sports.

    Returns:
        List of sport IDs that have implemented generators

    Example:
        >>> get_supported_sports()
        ['baseball', 'volleyball']
    """
    return ["baseball", "volleyball"]


def is_sport_supported(sport_id: str) -> bool:
    """
    Check if a sport is currently supported.

    Args:
        sport_id: Sport identifier to check

    Returns:
        True if sport has an implemented generator, False otherwise

    Example:
        >>> is_sport_supported("baseball")
        True
        >>> is_sport_supported("soccer")
        False
    """
    if not sport_id or not isinstance(sport_id, str):
        return False

    return sport_id.lower().strip() in get_supported_sports()
