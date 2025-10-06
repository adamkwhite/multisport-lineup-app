"""
Abstract base class for sport-specific lineup generators.

This module defines the interface that all sport-specific lineup generators
must implement, along with common validation and utility methods.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from sports.models.lineup import Lineup, Player
from sports.models.sport_config import SportConfig


class LineupGenerator(ABC):
    """
    Abstract base class for sport-specific lineup generators.

    Each sport implementation (baseball, soccer, volleyball) must inherit from
    this class and implement the generate() method with sport-specific logic.

    Attributes:
        config: SportConfig instance loaded from config/sports/{sport}.json
        required_positions: List of position IDs that must be filled
    """

    def __init__(self, sport_config: SportConfig):
        """
        Initialize generator with sport configuration.

        Args:
            sport_config: Configuration loaded from config/sports/{sport}.json
        """
        self.config = sport_config
        self.required_positions = sport_config.rules.required_positions

    @abstractmethod
    def generate(
        self,
        players: List[Player],
        game_info: dict,
        player_history: Optional[Dict] = None,
    ) -> List[Lineup]:
        """
        Generate lineups for all periods in a game.

        Args:
            players: List of available players for the game
            game_info: Game metadata dictionary with keys:
                      - game_id: Unique identifier for the game
                      - team_id: Team identifier
                      - num_periods: Number of periods to generate (optional)
            player_history: Optional dict tracking previous assignments across games
                          Format: {player_id: [positions played]}

        Returns:
            List of Lineup objects, one for each period of play

        Raises:
            ValueError: If insufficient players or required positions unavailable
        """
        pass

    def validate_players(self, players: List[Player]) -> List[str]:
        """
        Validate that players meet minimum sport requirements.

        Checks:
        - Sufficient number of players for full lineup
        - Required positions (pitcher, goalkeeper, setter, etc.) available
        - Player data is complete (has name, id)

        Args:
            players: List of players to validate

        Returns:
            List of validation error messages (empty list if valid)
        """
        errors = []

        # Check minimum players
        min_players = self.config.rules.total_positions
        if len(players) < min_players:
            errors.append(
                f"Insufficient players: need {min_players}, have {len(players)}"
            )

        # Check player data completeness
        for i, player in enumerate(players):
            if not player.id:
                errors.append(f"Player at index {i} missing ID")
            if not player.name:
                errors.append(f"Player at index {i} missing name")

        # Check required positions available
        for req_pos in self.required_positions:
            has_candidate = any(
                p.can_play_position(req_pos) for p in players
            )
            if not has_candidate:
                position_name = self._get_position_name(req_pos)
                errors.append(
                    f"No player available for required position: {position_name} ({req_pos})"
                )

        return errors

    def validate_lineup(self, lineup: Lineup) -> List[str]:
        """
        Validate a generated lineup meets sport rules.

        Checks:
        - All positions filled (correct number of assignments)
        - Required positions present (pitcher, goalkeeper, setter, etc.)
        - No duplicate players in same lineup
        - Position assignments are valid for the sport

        Args:
            lineup: Lineup to validate

        Returns:
            List of validation error messages (empty list if valid)
        """
        errors = []

        # Check all positions filled
        expected_positions = self.config.rules.total_positions
        actual_positions = len(lineup.assignments)
        if actual_positions != expected_positions:
            errors.append(
                f"Incomplete lineup: {actual_positions} positions filled, "
                f"need {expected_positions}"
            )

        # Check required positions present
        assigned_positions = {a.position for a in lineup.assignments}
        for req_pos in self.required_positions:
            if req_pos not in assigned_positions:
                position_name = self._get_position_name(req_pos)
                errors.append(
                    f"Required position not assigned: {position_name} ({req_pos})"
                )

        # Check no duplicate players (use lineup's built-in method)
        duplicate_errors = lineup.validate_no_duplicates()
        errors.extend(duplicate_errors)

        # Validate each position assignment
        for assignment in lineup.assignments:
            if not assignment.player.can_play_position(assignment.position):
                errors.append(
                    f"Player {assignment.player.name} cannot play position "
                    f"{assignment.position} (preferences: {assignment.player.position_preferences})"
                )

        return errors

    def get_available_players(
        self, players: List[Player], game_info: dict
    ) -> List[Player]:
        """
        Filter players by availability/attendance.

        Default implementation returns all players. Override in subclasses
        if attendance tracking is needed.

        Args:
            players: Full list of team players
            game_info: Game metadata (may include attendance data)

        Returns:
            List of available players
        """
        # Default: all players available
        # Subclasses can override to check game_info["attendance"] or similar
        return players

    def _get_position_name(self, position_id: str) -> str:
        """
        Get human-readable name for a position ID.

        Args:
            position_id: Position identifier (e.g., "P", "C", "GK")

        Returns:
            Position name (e.g., "Pitcher", "Catcher", "Goalkeeper")
        """
        position = self.config.get_position(position_id)
        if position:
            return position.name
        return position_id

    def _validate_game_info(self, game_info: dict) -> List[str]:
        """
        Validate game_info dictionary has required fields.

        Args:
            game_info: Game metadata dictionary

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []
        required_fields = ["game_id", "team_id"]

        for field in required_fields:
            if field not in game_info:
                errors.append(f"game_info missing required field: {field}")

        return errors
