"""
Sport configuration data models.

This module defines the data structures for sport-specific configurations
that are loaded from JSON files in config/sports/.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Position:
    """Represents a position in a sport."""

    id: str
    name: str
    abbrev: str
    required: bool = False
    max_per_lineup: Optional[int] = None


@dataclass
class GameStructure:
    """Defines the game structure (innings, halves, sets, etc.)."""

    type: str  # "innings", "halves", "sets"
    periods: int
    period_name: str  # "Inning", "Half", "Set"


@dataclass
class SportRules:
    """Sport-specific rules and constraints."""

    total_positions: int
    substitution_limit: Optional[int] = None
    required_positions: Optional[List[str]] = None
    rotation_type: str = "flexible"  # "flexible", "substitution_based", "rotation_based"
    generation_rules: Optional[Dict] = None

    def __post_init__(self):
        if self.required_positions is None:
            self.required_positions = []
        if self.generation_rules is None:
            self.generation_rules = {}


@dataclass
class FieldDiagram:
    """Field/court diagram specifications."""

    type: str  # "diamond", "rectangle", "court"
    width: int
    height: int
    position_coordinates: Dict[str, Dict[str, int]]


@dataclass
class SportConfig:
    """Complete configuration for a sport."""

    sport_id: str
    display_name: str
    positions: List[Position]
    game_structure: GameStructure
    rules: SportRules
    field_diagram: FieldDiagram

    def get_position(self, position_id: str) -> Optional[Position]:
        """Get a position by ID."""
        for position in self.positions:
            if position.id == position_id:
                return position
        return None

    def get_required_positions(self) -> List[Position]:
        """Get all required positions."""
        return [p for p in self.positions if p.required]

    def validate(self) -> List[str]:
        """
        Validate the configuration.

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Check that required positions exist
        position_ids = {p.id for p in self.positions}
        for req_pos in self.rules.required_positions:
            if req_pos not in position_ids:
                errors.append(
                    f"Required position '{req_pos}' not found in positions list"
                )

        # Check total_positions is reasonable (position types should be <= total slots)
        # Note: Some sports have position types that can have multiple players (e.g., CB, CM in soccer)
        # so we just check that we have at least one position type defined
        if len(self.positions) == 0:
            errors.append("No positions defined")

        # Optionally, check that max_per_lineup totals make sense
        # For sports like baseball where each position has max 1, this should match total_positions
        # For soccer, it's more flexible

        # Check field diagram has coordinates for all positions
        for position in self.positions:
            if position.id not in self.field_diagram.position_coordinates:
                errors.append(
                    f"Position '{position.id}' missing from field_diagram coordinates"
                )

        return errors
