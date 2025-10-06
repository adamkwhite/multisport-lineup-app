"""
Unit tests for sport configuration system.

Tests loading, validation, and caching of sport configurations.
"""

import json
import os
import sys
import tempfile
from unittest.mock import mock_open, patch

import pytest

# Add parent directory to path
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from sports.models.sport_config import (
    FieldDiagram,
    GameStructure,
    Position,
    SportConfig,
    SportRules,
)
from sports.services.sport_loader import (
    clear_cache,
    get_available_sports,
    get_config_path,
    load_sport_config,
)


class TestPosition:
    """Tests for Position dataclass."""

    def test_position_creation(self):
        """Test creating a Position."""
        pos = Position(
            id="P", name="Pitcher", abbrev="P", required=True, max_per_lineup=1
        )
        assert pos.id == "P"
        assert pos.name == "Pitcher"
        assert pos.abbrev == "P"
        assert pos.required is True
        assert pos.max_per_lineup == 1

    def test_position_defaults(self):
        """Test Position with default values."""
        pos = Position(id="LF", name="Left Field", abbrev="LF")
        assert pos.required is False
        assert pos.max_per_lineup is None


class TestGameStructure:
    """Tests for GameStructure dataclass."""

    def test_game_structure_creation(self):
        """Test creating a GameStructure."""
        gs = GameStructure(type="innings", periods=6, period_name="Inning")
        assert gs.type == "innings"
        assert gs.periods == 6
        assert gs.period_name == "Inning"


class TestSportRules:
    """Tests for SportRules dataclass."""

    def test_sport_rules_creation(self):
        """Test creating SportRules."""
        rules = SportRules(
            total_positions=9,
            substitution_limit=None,
            required_positions=["P", "C"],
            rotation_type="flexible",
        )
        assert rules.total_positions == 9
        assert rules.substitution_limit is None
        assert rules.required_positions == ["P", "C"]
        assert rules.rotation_type == "flexible"

    def test_sport_rules_defaults(self):
        """Test SportRules with default values."""
        rules = SportRules(total_positions=11)
        assert rules.required_positions == []
        assert rules.rotation_type == "flexible"


class TestFieldDiagram:
    """Tests for FieldDiagram dataclass."""

    def test_field_diagram_creation(self):
        """Test creating a FieldDiagram."""
        diagram = FieldDiagram(
            type="diamond",
            width=800,
            height=800,
            position_coordinates={"P": {"x": 400, "y": 520}},
        )
        assert diagram.type == "diamond"
        assert diagram.width == 800
        assert diagram.height == 800
        assert diagram.position_coordinates["P"]["x"] == 400


class TestSportConfig:
    """Tests for SportConfig dataclass."""

    def setup_method(self):
        """Set up test fixtures."""
        self.positions = [
            Position(id="P", name="Pitcher", abbrev="P", required=True),
            Position(id="C", name="Catcher", abbrev="C", required=True),
            Position(id="1B", name="First Base", abbrev="1B"),
        ]
        self.game_structure = GameStructure(
            type="innings", periods=6, period_name="Inning"
        )
        self.rules = SportRules(
            total_positions=3, required_positions=["P", "C"], rotation_type="flexible"
        )
        self.field_diagram = FieldDiagram(
            type="diamond",
            width=800,
            height=800,
            position_coordinates={
                "P": {"x": 400, "y": 520},
                "C": {"x": 400, "y": 650},
                "1B": {"x": 580, "y": 520},
            },
        )

    def test_sport_config_creation(self):
        """Test creating a SportConfig."""
        config = SportConfig(
            sport_id="baseball",
            display_name="Baseball",
            positions=self.positions,
            game_structure=self.game_structure,
            rules=self.rules,
            field_diagram=self.field_diagram,
        )
        assert config.sport_id == "baseball"
        assert config.display_name == "Baseball"
        assert len(config.positions) == 3

    def test_get_position(self):
        """Test get_position method."""
        config = SportConfig(
            sport_id="baseball",
            display_name="Baseball",
            positions=self.positions,
            game_structure=self.game_structure,
            rules=self.rules,
            field_diagram=self.field_diagram,
        )
        pos = config.get_position("P")
        assert pos is not None
        assert pos.name == "Pitcher"

        pos = config.get_position("NONEXISTENT")
        assert pos is None

    def test_get_required_positions(self):
        """Test get_required_positions method."""
        config = SportConfig(
            sport_id="baseball",
            display_name="Baseball",
            positions=self.positions,
            game_structure=self.game_structure,
            rules=self.rules,
            field_diagram=self.field_diagram,
        )
        required = config.get_required_positions()
        assert len(required) == 2
        assert all(p.required for p in required)

    def test_validate_success(self):
        """Test validation with valid configuration."""
        config = SportConfig(
            sport_id="baseball",
            display_name="Baseball",
            positions=self.positions,
            game_structure=self.game_structure,
            rules=self.rules,
            field_diagram=self.field_diagram,
        )
        errors = config.validate()
        assert errors == []

    def test_validate_missing_required_position(self):
        """Test validation fails when required position doesn't exist."""
        rules = SportRules(
            total_positions=3,
            required_positions=["P", "C", "SS"],  # SS doesn't exist
            rotation_type="flexible",
        )
        config = SportConfig(
            sport_id="baseball",
            display_name="Baseball",
            positions=self.positions,
            game_structure=self.game_structure,
            rules=rules,
            field_diagram=self.field_diagram,
        )
        errors = config.validate()
        assert len(errors) == 1
        assert "SS" in errors[0]

    def test_validate_no_positions(self):
        """Test validation fails when no positions defined."""
        config = SportConfig(
            sport_id="baseball",
            display_name="Baseball",
            positions=[],  # No positions
            game_structure=self.game_structure,
            rules=self.rules,
            field_diagram=self.field_diagram,
        )
        errors = config.validate()
        assert len(errors) >= 1
        assert any("No positions" in error for error in errors)

    def test_validate_missing_field_coordinates(self):
        """Test validation fails when field coordinates missing."""
        field_diagram = FieldDiagram(
            type="diamond",
            width=800,
            height=800,
            position_coordinates={
                "P": {"x": 400, "y": 520},
                # Missing C and 1B
            },
        )
        config = SportConfig(
            sport_id="baseball",
            display_name="Baseball",
            positions=self.positions,
            game_structure=self.game_structure,
            rules=self.rules,
            field_diagram=field_diagram,
        )
        errors = config.validate()
        assert len(errors) == 2  # Missing C and 1B


class TestSportLoader:
    """Tests for sport configuration loader."""

    def setup_method(self):
        """Set up test fixtures."""
        clear_cache()

    def teardown_method(self):
        """Clean up after tests."""
        clear_cache()

    def test_get_config_path(self):
        """Test get_config_path returns correct path."""
        path = get_config_path("baseball")
        assert path.endswith("config/sports/baseball.json")
        assert os.path.isabs(path)

    def test_load_baseball_config(self):
        """Test loading baseball configuration."""
        config = load_sport_config("baseball")
        assert config is not None
        assert config.sport_id == "baseball"
        assert config.display_name == "Baseball"
        assert len(config.positions) == 9
        assert config.game_structure.type == "innings"
        assert config.rules.total_positions == 9

    def test_load_soccer_config(self):
        """Test loading soccer configuration."""
        config = load_sport_config("soccer")
        assert config is not None
        assert config.sport_id == "soccer"
        assert config.display_name == "Soccer"
        assert len(config.positions) == 10  # 10 position types (GK, LB, CB, RB, LM, CM, RM, LW, RW, ST)
        assert config.game_structure.type == "halves"
        assert config.rules.total_positions == 11  # 11 players on field (CB and CM have 2 each)

    def test_load_volleyball_config(self):
        """Test loading volleyball configuration."""
        config = load_sport_config("volleyball")
        assert config is not None
        assert config.sport_id == "volleyball"
        assert config.display_name == "Volleyball"
        assert len(config.positions) == 6
        assert config.game_structure.type == "sets"
        assert config.rules.total_positions == 6

    def test_config_caching(self):
        """Test that configurations are cached."""
        config1 = load_sport_config("baseball", use_cache=True)
        config2 = load_sport_config("baseball", use_cache=True)
        assert config1 is config2  # Same object reference

    def test_bypass_cache(self):
        """Test loading without cache."""
        config1 = load_sport_config("baseball", use_cache=True)
        config2 = load_sport_config("baseball", use_cache=False)
        assert config1 is not config2  # Different objects

    def test_load_nonexistent_sport(self):
        """Test loading non-existent sport raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_sport_config("nonexistent")

    def test_get_available_sports(self):
        """Test getting list of available sports."""
        sports = get_available_sports()
        assert len(sports) >= 3
        sport_ids = {s["id"] for s in sports}
        assert "baseball" in sport_ids
        assert "soccer" in sport_ids
        assert "volleyball" in sport_ids

    def test_clear_cache(self):
        """Test clearing the cache."""
        config1 = load_sport_config("baseball")
        clear_cache()
        config2 = load_sport_config("baseball")
        assert config1 is not config2
