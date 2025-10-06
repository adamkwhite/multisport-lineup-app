"""
Unit tests for lineup utility functions.

Tests the smart position assignment algorithm and helper functions.
"""

import pytest

from sports.models.lineup import Player, PositionAssignment
from sports.models.sport_config import Position
from sports.utils.lineup_utils import (
    assign_positions_smart,
    calculate_position_balance,
    can_fill_all_positions,
    track_player_position_history,
    validate_lineup_completeness,
)


class TestCanFillAllPositions:
    """Tests for can_fill_all_positions function."""

    def test_can_fill_all_positions_sufficient_players(self):
        """Test with sufficient flexible players."""
        players = [
            Player(id="1", name="P1", position_preferences=[]),
            Player(id="2", name="P2", position_preferences=[]),
            Player(id="3", name="P3", position_preferences=[]),
        ]
        position_ids = ["P", "C", "1B"]
        assert can_fill_all_positions(players, position_ids)

    def test_can_fill_all_positions_exact_match(self):
        """Test with exact position preferences."""
        players = [
            Player(id="1", name="P1", position_preferences=["P"]),
            Player(id="2", name="P2", position_preferences=["C"]),
            Player(id="3", name="P3", position_preferences=["1B"]),
        ]
        position_ids = ["P", "C", "1B"]
        assert can_fill_all_positions(players, position_ids)

    def test_can_fill_all_positions_insufficient_players(self):
        """Test with too few players."""
        players = [
            Player(id="1", name="P1", position_preferences=[]),
            Player(id="2", name="P2", position_preferences=[]),
        ]
        position_ids = ["P", "C", "1B"]
        assert not can_fill_all_positions(players, position_ids)

    def test_can_fill_all_positions_impossible_constraints(self):
        """Test when position constraints make it impossible."""
        players = [
            Player(id="1", name="P1", position_preferences=["P"]),
            Player(id="2", name="P2", position_preferences=["P"]),
        ]
        position_ids = ["P", "C"]
        assert not can_fill_all_positions(players, position_ids)

    def test_can_fill_all_positions_empty(self):
        """Test with no positions to fill."""
        players = [Player(id="1", name="P1")]
        position_ids = []
        assert can_fill_all_positions(players, position_ids)


class TestAssignPositionsSmart:
    """Tests for assign_positions_smart function."""

    def test_assign_simple_case(self):
        """Test simple assignment with flexible players."""
        players = [
            Player(id="1", name="P1", position_preferences=[]),
            Player(id="2", name="P2", position_preferences=[]),
            Player(id="3", name="P3", position_preferences=[]),
        ]
        positions = [
            Position(id="P", name="Pitcher", abbrev="P"),
            Position(id="C", name="Catcher", abbrev="C"),
            Position(id="1B", name="First Base", abbrev="1B"),
        ]

        assignments = assign_positions_smart(players, positions)

        assert len(assignments) == 3
        assigned_positions = {a.position for a in assignments}
        assert assigned_positions == {"P", "C", "1B"}

    def test_assign_with_preferences(self):
        """Test assignment respects position preferences."""
        players = [
            Player(id="1", name="P1", position_preferences=["P"]),
            Player(id="2", name="P2", position_preferences=["C"]),
            Player(id="3", name="P3", position_preferences=[]),
        ]
        positions = [
            Position(id="P", name="Pitcher", abbrev="P"),
            Position(id="C", name="Catcher", abbrev="C"),
            Position(id="1B", name="First Base", abbrev="1B"),
        ]

        assignments = assign_positions_smart(players, positions)

        # Find assignments
        pitcher_assignment = next(a for a in assignments if a.position == "P")
        catcher_assignment = next(a for a in assignments if a.position == "C")

        assert pitcher_assignment.player.id == "1"
        assert catcher_assignment.player.id == "2"

    def test_assign_with_scarcity_priority(self):
        """Test that scarce positions are filled first."""
        players = [
            Player(id="1", name="P1", position_preferences=["P"]),  # Only pitcher
            Player(id="2", name="P2", position_preferences=["C", "1B"]),
            Player(id="3", name="P3", position_preferences=[]),
        ]
        positions = [
            Position(id="P", name="Pitcher", abbrev="P"),
            Position(id="C", name="Catcher", abbrev="C"),
            Position(id="1B", name="First Base", abbrev="1B"),
        ]

        assignments = assign_positions_smart(players, positions)

        # Pitcher should be assigned correctly despite scarcity
        pitcher_assignment = next(a for a in assignments if a.position == "P")
        assert pitcher_assignment.player.id == "1"

    def test_assign_with_must_play_players(self):
        """Test that must-play players get priority."""
        player1 = Player(id="1", name="P1", position_preferences=[])
        player2 = Player(id="2", name="P2", position_preferences=[])
        player3 = Player(id="3", name="P3", position_preferences=[])
        players = [player1, player2, player3]
        must_play = [player3]  # Player 3 must play

        positions = [
            Position(id="P", name="Pitcher", abbrev="P"),
            Position(id="C", name="Catcher", abbrev="C"),
        ]

        assignments = assign_positions_smart(
            players, positions, must_play_players=must_play
        )

        assigned_player_ids = {a.player.id for a in assignments}
        assert "3" in assigned_player_ids  # Player 3 must be assigned

    def test_assign_with_position_history(self):
        """Test that position history influences assignment."""
        players = [
            Player(id="1", name="P1", position_preferences=[]),
            Player(id="2", name="P2", position_preferences=[]),
        ]
        positions = [
            Position(id="P", name="Pitcher", abbrev="P"),
            Position(id="C", name="Catcher", abbrev="C"),
        ]

        # Player 1 has played pitcher many times
        history = {"1": ["P", "P", "P"], "2": ["C"]}

        assignments = assign_positions_smart(
            players, positions, player_position_history=history
        )

        # Player 1 should be assigned to a different position if possible
        player1_assignment = next(a for a in assignments if a.player.id == "1")
        # Due to rotation preference, player 1 should get catcher (less played)
        assert player1_assignment.position == "C"

    def test_assign_insufficient_players_raises_error(self):
        """Test that insufficient players raises ValueError."""
        players = [Player(id="1", name="P1", position_preferences=[])]
        positions = [
            Position(id="P", name="Pitcher", abbrev="P"),
            Position(id="C", name="Catcher", abbrev="C"),
        ]

        with pytest.raises(ValueError, match="Cannot fill all positions"):
            assign_positions_smart(players, positions)

    def test_assign_impossible_constraints_raises_error(self):
        """Test that impossible constraints raise ValueError."""
        players = [
            Player(id="1", name="P1", position_preferences=["P"]),
            Player(id="2", name="P2", position_preferences=["P"]),
        ]
        positions = [
            Position(id="P", name="Pitcher", abbrev="P"),
            Position(id="C", name="Catcher", abbrev="C"),
        ]

        with pytest.raises(ValueError, match="Cannot fill all positions"):
            assign_positions_smart(players, positions)


class TestTrackPlayerPositionHistory:
    """Tests for track_player_position_history function."""

    def test_track_empty_history(self):
        """Test tracking with empty history."""
        player = Player(id="1", name="P1")
        assignments = [PositionAssignment(player=player, position="P")]
        history = {}

        track_player_position_history(assignments, history)

        assert "1" in history
        assert history["1"] == ["P"]

    def test_track_existing_history(self):
        """Test tracking with existing history."""
        player = Player(id="1", name="P1")
        assignments = [PositionAssignment(player=player, position="C")]
        history = {"1": ["P", "1B"]}

        track_player_position_history(assignments, history)

        assert history["1"] == ["P", "1B", "C"]

    def test_track_multiple_assignments(self):
        """Test tracking multiple assignments at once."""
        player1 = Player(id="1", name="P1")
        player2 = Player(id="2", name="P2")
        assignments = [
            PositionAssignment(player=player1, position="P"),
            PositionAssignment(player=player2, position="C"),
        ]
        history = {}

        track_player_position_history(assignments, history)

        assert history["1"] == ["P"]
        assert history["2"] == ["C"]


class TestValidateLineupCompleteness:
    """Tests for validate_lineup_completeness function."""

    def test_validate_complete_lineup(self):
        """Test validating a complete lineup."""
        player1 = Player(id="1", name="P1")
        player2 = Player(id="2", name="P2")
        assignments = [
            PositionAssignment(player=player1, position="P"),
            PositionAssignment(player=player2, position="C"),
        ]
        required_positions = ["P", "C"]

        errors = validate_lineup_completeness(assignments, required_positions)

        assert errors == []

    def test_validate_missing_required_position(self):
        """Test validating lineup with missing required position."""
        player = Player(id="1", name="P1")
        assignments = [PositionAssignment(player=player, position="P")]
        required_positions = ["P", "C"]

        errors = validate_lineup_completeness(assignments, required_positions)

        assert len(errors) == 1
        assert "C" in errors[0]
        assert "Required position" in errors[0]

    def test_validate_duplicate_positions(self):
        """Test validating lineup with duplicate positions."""
        player1 = Player(id="1", name="P1")
        player2 = Player(id="2", name="P2")
        assignments = [
            PositionAssignment(player=player1, position="P"),
            PositionAssignment(player=player2, position="P"),
        ]
        required_positions = ["P"]

        errors = validate_lineup_completeness(assignments, required_positions)

        assert len(errors) == 1
        assert "assigned 2 times" in errors[0]


class TestCalculatePositionBalance:
    """Tests for calculate_position_balance function."""

    def test_calculate_balance_empty_history(self):
        """Test calculating balance with empty history."""
        history = {}
        balance = calculate_position_balance(history)
        assert balance == {}

    def test_calculate_balance_single_player(self):
        """Test calculating balance for single player."""
        history = {"1": ["P", "C", "P"]}
        balance = calculate_position_balance(history)
        assert balance["1"] == {"P": 2, "C": 1}

    def test_calculate_balance_multiple_players(self):
        """Test calculating balance for multiple players."""
        history = {"1": ["P", "P", "C"], "2": ["1B", "2B", "1B", "1B"]}
        balance = calculate_position_balance(history)
        assert balance["1"] == {"P": 2, "C": 1}
        assert balance["2"] == {"1B": 3, "2B": 1}

    def test_calculate_balance_filtered_players(self):
        """Test calculating balance for specific players only."""
        history = {"1": ["P", "C"], "2": ["1B", "2B"], "3": ["3B"]}
        balance = calculate_position_balance(history, player_ids=["1", "2"])
        assert "1" in balance
        assert "2" in balance
        assert "3" not in balance

    def test_calculate_balance_player_not_in_history(self):
        """Test calculating balance for player not in history."""
        history = {"1": ["P"]}
        balance = calculate_position_balance(history, player_ids=["1", "2"])
        assert balance["1"] == {"P": 1}
        assert balance["2"] == {}
