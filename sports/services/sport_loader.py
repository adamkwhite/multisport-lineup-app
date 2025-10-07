"""
Sport configuration loader service.

This module provides functions to load and cache sport configurations
from JSON files in the config/sports/ directory.
"""

import json
import os
from typing import Dict, Optional

from sports.models.sport_config import (
    FieldDiagram,
    GameStructure,
    Position,
    SportConfig,
    SportRules,
)

# Cache for loaded sport configurations
_config_cache: Dict[str, SportConfig] = {}


def get_config_path(sport_id: str) -> str:
    """
    Get the file path for a sport configuration.

    Args:
        sport_id: The sport identifier (e.g., "baseball", "soccer")

    Returns:
        Absolute path to the sport config JSON file
    """
    # Get the project root directory (2 levels up from this file)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_dir))
    return os.path.join(project_root, "config", "sports", f"{sport_id}.json")


def load_sport_config(sport_id: str, use_cache: bool = True) -> Optional[SportConfig]:
    """
    Load a sport configuration from JSON file.

    Args:
        sport_id: The sport identifier (e.g., "baseball", "soccer")
        use_cache: Whether to use cached configuration (default: True)

    Returns:
        SportConfig object if successful, None if file not found or invalid

    Raises:
        ValueError: If the configuration is invalid
        FileNotFoundError: If the configuration file doesn't exist
        json.JSONDecodeError: If the JSON is malformed
    """
    # Return cached config if available
    if use_cache and sport_id in _config_cache:
        return _config_cache[sport_id]

    config_path = get_config_path(sport_id)

    # Check if file exists
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Sport configuration not found: {config_path}")

    # Load and parse JSON
    with open(config_path, "r") as f:
        data = json.load(f)

    # Convert JSON to dataclass objects
    config = _parse_config(data)

    # Validate configuration
    errors = config.validate()
    if errors:
        raise ValueError(f"Invalid sport configuration: {', '.join(errors)}")

    # Cache the configuration
    _config_cache[sport_id] = config

    return config


def _parse_config(data: dict) -> SportConfig:
    """
    Parse JSON data into SportConfig dataclass.

    Args:
        data: Dictionary loaded from JSON file

    Returns:
        SportConfig object
    """
    # Parse positions
    positions = [
        Position(
            id=p["id"],
            name=p["name"],
            abbrev=p["abbrev"],
            required=p.get("required", False),
            max_per_lineup=p.get("max_per_lineup"),
        )
        for p in data["positions"]
    ]

    # Parse game structure
    game_structure = GameStructure(
        type=data["game_structure"]["type"],
        periods=data["game_structure"]["periods"],
        period_name=data["game_structure"]["period_name"],
    )

    # Parse rules
    rules = SportRules(
        total_positions=data["rules"]["total_positions"],
        substitution_limit=data["rules"].get("substitution_limit"),
        required_positions=data["rules"].get("required_positions", []),
        rotation_type=data["rules"].get("rotation_type", "flexible"),
    )

    # Parse field diagram
    field_diagram = FieldDiagram(
        type=data["field_diagram"]["type"],
        width=data["field_diagram"]["width"],
        height=data["field_diagram"]["height"],
        position_coordinates=data["field_diagram"]["position_coordinates"],
    )

    # Create and return SportConfig
    return SportConfig(
        sport_id=data["sport_id"],
        display_name=data["display_name"],
        positions=positions,
        game_structure=game_structure,
        rules=rules,
        field_diagram=field_diagram,
    )


def get_available_sports() -> list[dict]:
    """
    Get list of available sports.

    Returns:
        List of dicts with sport_id and display_name
    """
    sports = []
    config_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "config",
        "sports",
    )

    if os.path.exists(config_dir):
        for filename in os.listdir(config_dir):
            if filename.endswith(".json"):
                sport_id = filename[:-5]  # Remove .json extension
                try:
                    config = load_sport_config(sport_id)
                    sports.append(
                        {"id": config.sport_id, "name": config.display_name}
                    )
                except (FileNotFoundError, ValueError):
                    # Skip invalid configurations (ValueError includes JSONDecodeError)
                    continue

    return sports


def clear_cache():
    """Clear the configuration cache. Useful for testing."""
    global _config_cache
    _config_cache = {}
