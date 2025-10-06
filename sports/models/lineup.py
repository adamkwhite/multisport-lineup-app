"""
Lineup data models.

This module defines the data structures for lineup generation across all sports.
These models provide a common interface for player data, position assignments,
and complete lineups regardless of sport type.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Player:
    """
    Represents a player with position preferences.

    Attributes:
        id: Unique identifier (typically TeamSnap ID)
        name: Player's full name
        position_preferences: List of position IDs player can/wants to play
                            Empty list means player can play any position
        jersey_number: Optional jersey number for display
        metadata: Additional sport-specific data (attendance, skill level, etc.)
    """

    id: str
    name: str
    position_preferences: List[str] = field(default_factory=list)
    jersey_number: Optional[int] = None
    metadata: Dict = field(default_factory=dict)

    def can_play_position(self, position_id: str) -> bool:
        """Check if player can play a given position."""
        # Empty preferences means player can play anywhere
        if not self.position_preferences:
            return True
        return position_id in self.position_preferences

    def has_preference_for(self, position_id: str) -> bool:
        """Check if player has explicitly listed a position preference."""
        return position_id in self.position_preferences

    @classmethod
    def from_dict(cls, data: dict) -> "Player":
        """
        Create Player from dictionary (typically from API response).

        Args:
            data: Dictionary with keys: id, name, position_preferences (optional),
                  jersey_number (optional), and any other metadata

        Returns:
            Player instance
        """
        return cls(
            id=str(data["id"]),
            name=data["name"],
            position_preferences=data.get("position_preferences", []),
            jersey_number=data.get("jersey_number"),
            metadata={k: v for k, v in data.items()
                     if k not in ["id", "name", "position_preferences", "jersey_number"]},
        )

    def to_dict(self) -> dict:
        """Convert Player to dictionary for serialization."""
        result = {
            "id": self.id,
            "name": self.name,
            "position_preferences": self.position_preferences,
        }
        if self.jersey_number is not None:
            result["jersey_number"] = self.jersey_number
        if self.metadata:
            result.update(self.metadata)
        return result


@dataclass
class PositionAssignment:
    """
    Represents a player assigned to a position in a lineup.

    Attributes:
        player: The Player assigned to this position
        position: Position ID (e.g., "P", "C", "GK", "S")
        batting_order: Optional batting order position (baseball-specific)
        is_captain: Whether player is captain for this period
        notes: Additional notes (e.g., "Resting from catcher")
    """

    player: Player
    position: str
    batting_order: Optional[int] = None
    is_captain: bool = False
    notes: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert PositionAssignment to dictionary for serialization."""
        result = {
            "player": self.player.to_dict(),
            "position": self.position,
        }
        if self.batting_order is not None:
            result["batting_order"] = self.batting_order
        if self.is_captain:
            result["is_captain"] = self.is_captain
        if self.notes:
            result["notes"] = self.notes
        return result


@dataclass
class Lineup:
    """
    Represents a complete lineup for one period of play.

    Attributes:
        period: Period number (1-based: 1, 2, 3, etc.)
        period_name: Human-readable period name ("Inning 1-2", "Half 1", "Set 1")
        assignments: List of position assignments for this period
        bench_players: Players not assigned to positions this period
        substitutions_used: Number of substitutions used to create this lineup
        metadata: Additional sport-specific data
    """

    period: int
    period_name: str
    assignments: List[PositionAssignment] = field(default_factory=list)
    bench_players: List[Player] = field(default_factory=list)
    substitutions_used: int = 0
    metadata: Dict = field(default_factory=dict)

    def get_assigned_players(self) -> List[Player]:
        """Get list of all players assigned to positions."""
        return [assignment.player for assignment in self.assignments]

    def get_assigned_player_ids(self) -> set:
        """Get set of all player IDs assigned to positions."""
        return {assignment.player.id for assignment in self.assignments}

    def get_position_assignment(self, position_id: str) -> Optional[PositionAssignment]:
        """Get the assignment for a specific position."""
        for assignment in self.assignments:
            if assignment.position == position_id:
                return assignment
        return None

    def has_position_filled(self, position_id: str) -> bool:
        """Check if a position is filled in this lineup."""
        return self.get_position_assignment(position_id) is not None

    def validate_no_duplicates(self) -> List[str]:
        """
        Validate that no player is assigned to multiple positions.

        Returns:
            List of error messages (empty if valid)
        """
        errors = []
        player_ids = [a.player.id for a in self.assignments]
        seen = set()
        duplicates = set()

        for player_id in player_ids:
            if player_id in seen:
                duplicates.add(player_id)
            seen.add(player_id)

        if duplicates:
            duplicate_names = [
                a.player.name
                for a in self.assignments
                if a.player.id in duplicates
            ]
            errors.append(
                f"Players assigned to multiple positions: {', '.join(set(duplicate_names))}"
            )

        return errors

    def to_dict(self) -> dict:
        """Convert Lineup to dictionary for serialization."""
        return {
            "period": self.period,
            "period_name": self.period_name,
            "assignments": [a.to_dict() for a in self.assignments],
            "bench_players": [p.to_dict() for p in self.bench_players],
            "substitutions_used": self.substitutions_used,
            "metadata": self.metadata,
        }
