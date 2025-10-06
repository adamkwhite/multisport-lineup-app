"""
Unit tests for lineup data models.

Tests Player, PositionAssignment, and Lineup dataclasses.
"""

import pytest

from sports.models.lineup import Lineup, Player, PositionAssignment


class TestPlayer:
    """Tests for Player dataclass."""

    def test_player_creation(self):
        """Test creating a player with basic info."""
        player = Player(id="1", name="John Doe")
        assert player.id == "1"
        assert player.name == "John Doe"
        assert player.position_preferences == []
        assert player.jersey_number is None
        assert player.metadata == {}

    def test_player_with_preferences(self):
        """Test creating a player with position preferences."""
        player = Player(
            id="2",
            name="Jane Smith",
            position_preferences=["P", "1B"],
            jersey_number=42,
        )
        assert player.position_preferences == ["P", "1B"]
        assert player.jersey_number == 42

    def test_can_play_position_empty_preferences(self):
        """Test that player with empty preferences can play any position."""
        player = Player(id="1", name="John Doe", position_preferences=[])
        assert player.can_play_position("P")
        assert player.can_play_position("C")
        assert player.can_play_position("1B")

    def test_can_play_position_with_preferences(self):
        """Test that player with preferences can only play those positions."""
        player = Player(id="2", name="Jane Smith", position_preferences=["P", "1B"])
        assert player.can_play_position("P")
        assert player.can_play_position("1B")
        assert not player.can_play_position("C")

    def test_has_preference_for(self):
        """Test checking explicit preference."""
        player = Player(id="1", name="John Doe", position_preferences=["P"])
        assert player.has_preference_for("P")
        assert not player.has_preference_for("C")

    def test_has_preference_for_empty_preferences(self):
        """Test has_preference_for with empty preferences list."""
        player = Player(id="1", name="John Doe")
        assert not player.has_preference_for("P")

    def test_from_dict(self):
        """Test creating player from dictionary."""
        data = {
            "id": "123",
            "name": "Bob Jones",
            "position_preferences": ["C", "1B"],
            "jersey_number": 7,
            "extra_field": "extra_value",
        }
        player = Player.from_dict(data)
        assert player.id == "123"
        assert player.name == "Bob Jones"
        assert player.position_preferences == ["C", "1B"]
        assert player.jersey_number == 7
        assert player.metadata["extra_field"] == "extra_value"

    def test_from_dict_minimal(self):
        """Test creating player from minimal dictionary."""
        data = {"id": 456, "name": "Alice Brown"}
        player = Player.from_dict(data)
        assert player.id == "456"
        assert player.name == "Alice Brown"
        assert player.position_preferences == []
        assert player.jersey_number is None

    def test_to_dict(self):
        """Test converting player to dictionary."""
        player = Player(
            id="789",
            name="Charlie Davis",
            position_preferences=["P"],
            jersey_number=99,
            metadata={"skill_level": "advanced"},
        )
        result = player.to_dict()
        assert result["id"] == "789"
        assert result["name"] == "Charlie Davis"
        assert result["position_preferences"] == ["P"]
        assert result["jersey_number"] == 99
        assert result["skill_level"] == "advanced"

    def test_to_dict_minimal(self):
        """Test converting minimal player to dictionary."""
        player = Player(id="1", name="Test Player")
        result = player.to_dict()
        assert result == {"id": "1", "name": "Test Player", "position_preferences": []}


class TestPositionAssignment:
    """Tests for PositionAssignment dataclass."""

    def test_assignment_creation(self):
        """Test creating a position assignment."""
        player = Player(id="1", name="John Doe")
        assignment = PositionAssignment(player=player, position="P")
        assert assignment.player == player
        assert assignment.position == "P"
        assert assignment.batting_order is None
        assert assignment.is_captain is False
        assert assignment.notes is None

    def test_assignment_with_batting_order(self):
        """Test assignment with batting order (baseball-specific)."""
        player = Player(id="1", name="John Doe")
        assignment = PositionAssignment(player=player, position="P", batting_order=1)
        assert assignment.batting_order == 1

    def test_assignment_with_captain(self):
        """Test assignment with captain flag."""
        player = Player(id="1", name="John Doe")
        assignment = PositionAssignment(player=player, position="GK", is_captain=True)
        assert assignment.is_captain is True

    def test_assignment_with_notes(self):
        """Test assignment with notes."""
        player = Player(id="1", name="John Doe")
        assignment = PositionAssignment(
            player=player, position="C", notes="Resting from pitcher"
        )
        assert assignment.notes == "Resting from pitcher"

    def test_to_dict(self):
        """Test converting assignment to dictionary."""
        player = Player(id="1", name="John Doe")
        assignment = PositionAssignment(
            player=player,
            position="P",
            batting_order=5,
            is_captain=True,
            notes="Test note",
        )
        result = assignment.to_dict()
        assert result["player"]["id"] == "1"
        assert result["position"] == "P"
        assert result["batting_order"] == 5
        assert result["is_captain"] is True
        assert result["notes"] == "Test note"


class TestLineup:
    """Tests for Lineup dataclass."""

    def test_lineup_creation(self):
        """Test creating an empty lineup."""
        lineup = Lineup(period=1, period_name="Inning 1-2")
        assert lineup.period == 1
        assert lineup.period_name == "Inning 1-2"
        assert lineup.assignments == []
        assert lineup.bench_players == []
        assert lineup.substitutions_used == 0
        assert lineup.metadata == {}

    def test_lineup_with_assignments(self):
        """Test creating lineup with assignments."""
        player1 = Player(id="1", name="Player 1")
        player2 = Player(id="2", name="Player 2")
        assignment1 = PositionAssignment(player=player1, position="P")
        assignment2 = PositionAssignment(player=player2, position="C")

        lineup = Lineup(
            period=1, period_name="Inning 1-2", assignments=[assignment1, assignment2]
        )
        assert len(lineup.assignments) == 2
        assert lineup.assignments[0].position == "P"
        assert lineup.assignments[1].position == "C"

    def test_get_assigned_players(self):
        """Test getting list of assigned players."""
        player1 = Player(id="1", name="Player 1")
        player2 = Player(id="2", name="Player 2")
        assignment1 = PositionAssignment(player=player1, position="P")
        assignment2 = PositionAssignment(player=player2, position="C")

        lineup = Lineup(
            period=1, period_name="Test", assignments=[assignment1, assignment2]
        )
        players = lineup.get_assigned_players()
        assert len(players) == 2
        assert player1 in players
        assert player2 in players

    def test_get_assigned_player_ids(self):
        """Test getting set of assigned player IDs."""
        player1 = Player(id="1", name="Player 1")
        player2 = Player(id="2", name="Player 2")
        assignment1 = PositionAssignment(player=player1, position="P")
        assignment2 = PositionAssignment(player=player2, position="C")

        lineup = Lineup(
            period=1, period_name="Test", assignments=[assignment1, assignment2]
        )
        player_ids = lineup.get_assigned_player_ids()
        assert player_ids == {"1", "2"}

    def test_get_position_assignment(self):
        """Test getting assignment for specific position."""
        player = Player(id="1", name="Player 1")
        assignment = PositionAssignment(player=player, position="P")

        lineup = Lineup(period=1, period_name="Test", assignments=[assignment])
        result = lineup.get_position_assignment("P")
        assert result == assignment
        assert lineup.get_position_assignment("C") is None

    def test_has_position_filled(self):
        """Test checking if position is filled."""
        player = Player(id="1", name="Player 1")
        assignment = PositionAssignment(player=player, position="P")

        lineup = Lineup(period=1, period_name="Test", assignments=[assignment])
        assert lineup.has_position_filled("P")
        assert not lineup.has_position_filled("C")

    def test_validate_no_duplicates_valid(self):
        """Test validating lineup with no duplicate players."""
        player1 = Player(id="1", name="Player 1")
        player2 = Player(id="2", name="Player 2")
        assignment1 = PositionAssignment(player=player1, position="P")
        assignment2 = PositionAssignment(player=player2, position="C")

        lineup = Lineup(
            period=1, period_name="Test", assignments=[assignment1, assignment2]
        )
        errors = lineup.validate_no_duplicates()
        assert errors == []

    def test_validate_no_duplicates_invalid(self):
        """Test validating lineup with duplicate players."""
        player = Player(id="1", name="Player 1")
        assignment1 = PositionAssignment(player=player, position="P")
        assignment2 = PositionAssignment(player=player, position="C")

        lineup = Lineup(
            period=1, period_name="Test", assignments=[assignment1, assignment2]
        )
        errors = lineup.validate_no_duplicates()
        assert len(errors) == 1
        assert "Player 1" in errors[0]
        assert "multiple positions" in errors[0]

    def test_to_dict(self):
        """Test converting lineup to dictionary."""
        player = Player(id="1", name="Player 1")
        bench_player = Player(id="2", name="Player 2")
        assignment = PositionAssignment(player=player, position="P")

        lineup = Lineup(
            period=1,
            period_name="Inning 1-2",
            assignments=[assignment],
            bench_players=[bench_player],
            substitutions_used=1,
            metadata={"test": "value"},
        )
        result = lineup.to_dict()

        assert result["period"] == 1
        assert result["period_name"] == "Inning 1-2"
        assert len(result["assignments"]) == 1
        assert len(result["bench_players"]) == 1
        assert result["substitutions_used"] == 1
        assert result["metadata"]["test"] == "value"
