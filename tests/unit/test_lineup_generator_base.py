"""
Unit tests for LineupGenerator abstract base class.

Tests validation methods and abstract class contract.
"""

import pytest

from sports.generators.base import LineupGenerator
from sports.models.lineup import Lineup, Player, PositionAssignment
from sports.models.sport_config import (
    FieldDiagram,
    GameStructure,
    Position,
    SportConfig,
    SportRules,
)


# Create a concrete implementation for testing
class TestLineupGenerator(LineupGenerator):
    """Concrete implementation of LineupGenerator for testing."""

    def generate(self, players, game_info, player_history=None):
        """Simple implementation that just assigns players to positions."""
        assignments = []
        for i, position in enumerate(self.config.positions):
            if i < len(players):
                assignment = PositionAssignment(player=players[i], position=position.id)
                assignments.append(assignment)

        lineup = Lineup(period=1, period_name="Test Period", assignments=assignments)
        return [lineup]


@pytest.fixture
def baseball_config():
    """Create a baseball sport configuration for testing."""
    positions = [
        Position(id="P", name="Pitcher", abbrev="P", required=True),
        Position(id="C", name="Catcher", abbrev="C", required=True),
        Position(id="1B", name="First Base", abbrev="1B"),
        Position(id="2B", name="Second Base", abbrev="2B"),
    ]

    game_structure = GameStructure(type="innings", periods=6, period_name="Inning")

    rules = SportRules(
        total_positions=4, required_positions=["P", "C"], rotation_type="flexible"
    )

    field_diagram = FieldDiagram(
        type="diamond",
        width=800,
        height=800,
        position_coordinates={
            "P": {"x": 400, "y": 520},
            "C": {"x": 400, "y": 650},
            "1B": {"x": 580, "y": 520},
            "2B": {"x": 480, "y": 400},
        },
    )

    return SportConfig(
        sport_id="baseball",
        display_name="Baseball",
        positions=positions,
        game_structure=game_structure,
        rules=rules,
        field_diagram=field_diagram,
    )


@pytest.fixture
def generator(baseball_config):
    """Create a test lineup generator."""
    return TestLineupGenerator(baseball_config)


@pytest.fixture
def valid_players():
    """Create a set of valid players for testing."""
    return [
        Player(id="1", name="Player 1", position_preferences=["P"]),
        Player(id="2", name="Player 2", position_preferences=["C"]),
        Player(id="3", name="Player 3", position_preferences=["1B"]),
        Player(id="4", name="Player 4", position_preferences=["2B"]),
    ]


class TestLineupGeneratorConstruction:
    """Tests for LineupGenerator construction."""

    def test_constructor_sets_config(self, baseball_config):
        """Test that constructor sets config attribute."""
        generator = TestLineupGenerator(baseball_config)
        assert generator.config == baseball_config

    def test_constructor_sets_required_positions(self, baseball_config):
        """Test that constructor extracts required positions."""
        generator = TestLineupGenerator(baseball_config)
        assert generator.required_positions == ["P", "C"]

    def test_cannot_instantiate_abstract_class(self):
        """Test that abstract LineupGenerator cannot be instantiated."""
        config = SportConfig(
            sport_id="test",
            display_name="Test",
            positions=[],
            game_structure=GameStructure(type="test", periods=1, period_name="Test"),
            rules=SportRules(total_positions=1),
            field_diagram=FieldDiagram(
                type="test", width=100, height=100, position_coordinates={}
            ),
        )

        with pytest.raises(TypeError):
            LineupGenerator(config)


class TestValidatePlayers:
    """Tests for validate_players method."""

    def test_validate_sufficient_players(self, generator, valid_players):
        """Test validation passes with sufficient players."""
        errors = generator.validate_players(valid_players)
        assert errors == []

    def test_validate_insufficient_players(self, generator):
        """Test validation fails with insufficient players."""
        players = [
            Player(id="1", name="P1", position_preferences=[]),
            Player(id="2", name="P2", position_preferences=[]),
        ]
        errors = generator.validate_players(players)
        assert len(errors) > 0
        assert "Insufficient players" in errors[0]
        assert "need 4" in errors[0]
        assert "have 2" in errors[0]

    def test_validate_missing_required_position(self, generator):
        """Test validation fails when required position unavailable."""
        players = [
            Player(id="1", name="P1", position_preferences=["1B"]),
            Player(id="2", name="P2", position_preferences=["2B"]),
            Player(id="3", name="P3", position_preferences=["1B"]),
            Player(id="4", name="P4", position_preferences=["2B"]),
        ]
        errors = generator.validate_players(players)
        assert len(errors) > 0
        assert any("Pitcher" in error or "P" in error for error in errors)
        assert any("Catcher" in error or "C" in error for error in errors)

    def test_validate_player_missing_id(self, generator):
        """Test validation fails when player missing ID."""
        players = [
            Player(id="", name="P1", position_preferences=[]),
            Player(id="2", name="P2", position_preferences=[]),
            Player(id="3", name="P3", position_preferences=[]),
            Player(id="4", name="P4", position_preferences=[]),
        ]
        errors = generator.validate_players(players)
        assert len(errors) > 0
        assert any("missing ID" in error for error in errors)

    def test_validate_player_missing_name(self, generator):
        """Test validation fails when player missing name."""
        players = [
            Player(id="1", name="", position_preferences=[]),
            Player(id="2", name="P2", position_preferences=[]),
            Player(id="3", name="P3", position_preferences=[]),
            Player(id="4", name="P4", position_preferences=[]),
        ]
        errors = generator.validate_players(players)
        assert len(errors) > 0
        assert any("missing name" in error for error in errors)


class TestValidateLineup:
    """Tests for validate_lineup method."""

    def test_validate_complete_lineup(self, generator, valid_players):
        """Test validation passes for complete lineup."""
        assignments = [
            PositionAssignment(player=valid_players[0], position="P"),
            PositionAssignment(player=valid_players[1], position="C"),
            PositionAssignment(player=valid_players[2], position="1B"),
            PositionAssignment(player=valid_players[3], position="2B"),
        ]
        lineup = Lineup(period=1, period_name="Test", assignments=assignments)

        errors = generator.validate_lineup(lineup)
        assert errors == []

    def test_validate_incomplete_lineup(self, generator, valid_players):
        """Test validation fails for incomplete lineup."""
        assignments = [
            PositionAssignment(player=valid_players[0], position="P"),
            PositionAssignment(player=valid_players[1], position="C"),
        ]
        lineup = Lineup(period=1, period_name="Test", assignments=assignments)

        errors = generator.validate_lineup(lineup)
        assert len(errors) > 0
        assert any("Incomplete lineup" in error for error in errors)
        assert any("2 positions filled" in error for error in errors)

    def test_validate_missing_required_position(self, generator, valid_players):
        """Test validation fails when required position not assigned."""
        assignments = [
            PositionAssignment(player=valid_players[0], position="P"),
            PositionAssignment(player=valid_players[2], position="1B"),
            PositionAssignment(player=valid_players[3], position="2B"),
        ]
        # Missing catcher, but still have 4 positions to trick the count check
        assignments.append(
            PositionAssignment(
                player=Player(id="5", name="P5", position_preferences=[]),
                position="1B",
            )
        )
        lineup = Lineup(period=1, period_name="Test", assignments=assignments)

        errors = generator.validate_lineup(lineup)
        # Should have error about missing catcher
        assert any("Catcher" in error or "C" in error for error in errors)

    def test_validate_duplicate_players(self, generator, valid_players):
        """Test validation fails with duplicate players."""
        player = valid_players[0]
        assignments = [
            PositionAssignment(player=player, position="P"),
            PositionAssignment(player=player, position="C"),
            PositionAssignment(player=valid_players[2], position="1B"),
            PositionAssignment(player=valid_players[3], position="2B"),
        ]
        lineup = Lineup(period=1, period_name="Test", assignments=assignments)

        errors = generator.validate_lineup(lineup)
        assert len(errors) > 0
        assert any("multiple positions" in error for error in errors)

    def test_validate_player_cannot_play_position(self, generator):
        """Test validation fails when player assigned to incompatible position."""
        players = [
            Player(id="1", name="P1", position_preferences=["P"]),
            Player(id="2", name="P2", position_preferences=["C"]),
            Player(id="3", name="P3", position_preferences=["1B"]),
            Player(id="4", name="P4", position_preferences=["2B"]),
        ]
        # Assign pitcher to catcher position
        assignments = [
            PositionAssignment(player=players[0], position="C"),
            PositionAssignment(player=players[1], position="P"),
            PositionAssignment(player=players[2], position="1B"),
            PositionAssignment(player=players[3], position="2B"),
        ]
        lineup = Lineup(period=1, period_name="Test", assignments=assignments)

        errors = generator.validate_lineup(lineup)
        assert len(errors) > 0
        assert any("cannot play position" in error for error in errors)


class TestGetAvailablePlayers:
    """Tests for get_available_players method."""

    def test_get_available_players_default(self, generator, valid_players):
        """Test default implementation returns all players."""
        game_info = {"game_id": "123", "team_id": "456"}
        available = generator.get_available_players(valid_players, game_info)
        assert available == valid_players


class TestPrivateMethods:
    """Tests for private helper methods."""

    def test_get_position_name(self, generator):
        """Test getting position name from ID."""
        name = generator._get_position_name("P")
        assert name == "Pitcher"

        name = generator._get_position_name("C")
        assert name == "Catcher"

    def test_get_position_name_unknown(self, generator):
        """Test getting name for unknown position returns ID."""
        name = generator._get_position_name("UNKNOWN")
        assert name == "UNKNOWN"

    def test_validate_game_info_valid(self, generator):
        """Test validating game_info with required fields."""
        game_info = {"game_id": "123", "team_id": "456"}
        errors = generator._validate_game_info(game_info)
        assert errors == []

    def test_validate_game_info_missing_fields(self, generator):
        """Test validating game_info with missing fields."""
        game_info = {"game_id": "123"}
        errors = generator._validate_game_info(game_info)
        assert len(errors) > 0
        assert any("team_id" in error for error in errors)

    def test_validate_game_info_empty(self, generator):
        """Test validating empty game_info."""
        game_info = {}
        errors = generator._validate_game_info(game_info)
        assert len(errors) == 2  # Missing both required fields
