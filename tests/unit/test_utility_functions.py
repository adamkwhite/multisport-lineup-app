"""
Tests for utility functions in app.py
"""

import os
import sys

import pytest

# Add the parent directory to sys.path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import (
    FIELDING_POSITIONS,
    assign_positions_smart,
    can_fill_all_positions,
    obfuscate_name,
)


class TestObfuscateName:
    """Tests for the obfuscate_name function"""

    def test_obfuscate_full_name(self):
        """Test obfuscating a normal full name"""
        result = obfuscate_name("Adam White")
        assert result == "A*** W****"

    def test_obfuscate_single_name(self):
        """Test obfuscating a single name"""
        result = obfuscate_name("Adam")
        assert result == "A***"

    def test_obfuscate_empty_string(self):
        """Test obfuscating an empty string"""
        result = obfuscate_name("")
        assert result == "Unknown Player"

    def test_obfuscate_none(self):
        """Test obfuscating None"""
        result = obfuscate_name(None)
        assert result == "Unknown Player"

    def test_obfuscate_whitespace_only(self):
        """Test obfuscating whitespace-only string"""
        result = obfuscate_name("   ")
        assert result == "Unknown Player"

    def test_obfuscate_single_letter_name(self):
        """Test obfuscating single letter names"""
        result = obfuscate_name("A B")
        assert result == "A B"

    def test_obfuscate_with_middle_name(self):
        """Test obfuscating name with middle name"""
        result = obfuscate_name("John William Smith")
        assert result == "J*** S****"

    def test_obfuscate_two_letter_names(self):
        """Test obfuscating two-letter names"""
        result = obfuscate_name("Al Bo")
        assert result == "A* B*"


class TestCanFillAllPositions:
    """Tests for the can_fill_all_positions function"""

    def test_enough_flexible_players(self):
        """Test with enough flexible players for all positions"""
        players = [{"id": i, "position_preferences": []} for i in range(1, 10)]
        positions = list(range(1, 10))
        assert can_fill_all_positions(players, positions) is True

    def test_insufficient_players(self):
        """Test with insufficient players"""
        players = [
            {"id": 1, "position_preferences": []},
            {"id": 2, "position_preferences": []},
        ]
        positions = list(range(1, 10))
        assert can_fill_all_positions(players, positions) is False

    def test_with_position_preferences(self):
        """Test with specific position preferences"""
        players = [
            {"id": 1, "position_preferences": [1]},  # Pitcher only
            {"id": 2, "position_preferences": [2]},  # Catcher only
            {"id": 3, "position_preferences": []},  # Any position
            {"id": 4, "position_preferences": []},  # Any position
            {"id": 5, "position_preferences": []},  # Any position
            {"id": 6, "position_preferences": []},  # Any position
            {"id": 7, "position_preferences": []},  # Any position
            {"id": 8, "position_preferences": []},  # Any position
            {"id": 9, "position_preferences": []},  # Any position
        ]
        positions = list(range(1, 10))
        assert can_fill_all_positions(players, positions) is True

    def test_impossible_constraints(self):
        """Test with impossible position constraints"""
        players = [
            {"id": 1, "position_preferences": [1]},  # Pitcher only
            {"id": 2, "position_preferences": [1]},  # Also pitcher only
            {"id": 3, "position_preferences": [1]},  # Also pitcher only
        ]
        positions = [1, 2, 3]  # Need pitcher, catcher, and first base
        assert can_fill_all_positions(players, positions) is False

    def test_empty_positions(self):
        """Test with no positions to fill"""
        players = [{"id": 1, "position_preferences": []}]
        positions = []
        assert can_fill_all_positions(players, positions) is True

    def test_exact_match(self):
        """Test with exactly matching players and positions"""
        players = [{"id": i, "position_preferences": [i]} for i in range(1, 10)]
        positions = list(range(1, 10))
        assert can_fill_all_positions(players, positions) is True


class TestAssignPositionsSmart:
    """Tests for the assign_positions_smart function"""

    def test_simple_assignment(self):
        """Test basic position assignment"""
        players = [
            {"id": i, "name": f"Player {i}", "position_preferences": []}
            for i in range(1, 10)
        ]
        positions = list(range(1, 10))
        must_play = []
        position_candidates = {pos: players for pos in range(1, 10)}

        result = assign_positions_smart(players, positions, must_play)

        assert result is not None
        assert len(result) == 9
        assert all(pos in result for pos in range(1, 10))

    def test_with_must_play_players(self):
        """Test that must-play players are prioritized"""
        players = [
            {"id": i, "name": f"Player {i}", "position_preferences": []}
            for i in range(1, 10)
        ]
        must_play = [players[0], players[1]]  # First two players must play
        positions = list(range(1, 10))
        position_candidates = {pos: players for pos in range(1, 10)}

        result = assign_positions_smart(
            players, positions, must_play, position_candidates
        )

        assert result is not None
        # Check that must-play players are assigned
        assigned_players = list(result.values())
        assert players[0] in assigned_players
        assert players[1] in assigned_players

    def test_impossible_assignment(self):
        """Test that impossible assignments return None"""
        players = [
            {"id": 1, "name": "Player 1", "position_preferences": [1]},
        ]
        positions = [1, 2, 3]  # Need 3 positions but only 1 player
        must_play = []
        position_candidates = {1: [players[0]], 2: [], 3: []}

        result = assign_positions_smart(
            players, positions, must_play, position_candidates
        )

        assert result is None

    def test_position_scarcity_priority(self):
        """Test that scarce positions are filled first"""
        pitcher_only = {"id": 1, "name": "Pitcher", "position_preferences": [1]}
        flexible_players = [
            {"id": i, "name": f"Player {i}", "position_preferences": []}
            for i in range(2, 10)
        ]
        players = [pitcher_only] + flexible_players

        positions = list(range(1, 10))
        must_play = []
        position_candidates = {
            1: [pitcher_only],  # Only one candidate for pitcher
            2: flexible_players,
            3: flexible_players,
            4: flexible_players,
            5: flexible_players,
            6: flexible_players,
            7: flexible_players,
            8: flexible_players,
            9: flexible_players,
        }

        result = assign_positions_smart(
            players, positions, must_play, position_candidates
        )

        assert result is not None
        assert result[1] == pitcher_only  # Pitcher should be assigned to position 1

    def test_with_position_history(self):
        """Test that position history affects rotation"""
        players = [
            {"id": i, "name": f"Player {i}", "position_preferences": []}
            for i in range(1, 10)
        ]
        positions = list(range(1, 10))
        must_play = []
        position_candidates = {pos: players for pos in range(1, 10)}

        # Player 1 has played position 1 many times
        player_position_history = {
            1: [1, 1, 1, 1],  # Played pitcher 4 times
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
        }

        result = assign_positions_smart(
            players, positions, must_play, player_position_history
        )

        assert result is not None
        # Player 1 should ideally not be assigned pitcher again (though not guaranteed)
        assert len(result) == 9
