"""
Tests for sport-specific generation rules.

Tests that generation rules are properly loaded from config files and
enforced by lineup generators.
"""

import pytest

from sports.services.sport_loader import load_sport_config


class TestBaseballGenerationRules:
    """Tests for baseball generation rules."""

    def test_baseball_config_has_generation_rules(self):
        """Test that baseball config includes generation_rules."""
        config = load_sport_config("baseball")

        assert hasattr(config.rules, "generation_rules")
        assert config.rules.generation_rules is not None
        assert isinstance(config.rules.generation_rules, dict)

    def test_baseball_pitcher_max_innings_rule(self):
        """Test that pitcher_max_consecutive_innings is defined."""
        config = load_sport_config("baseball")

        assert "pitcher_max_consecutive_innings" in config.rules.generation_rules
        assert config.rules.generation_rules["pitcher_max_consecutive_innings"] == 2

    def test_baseball_min_players_rule(self):
        """Test that min_players_required is defined."""
        config = load_sport_config("baseball")

        assert "min_players_required" in config.rules.generation_rules
        assert config.rules.generation_rules["min_players_required"] == 9

    def test_baseball_rotation_encouraged_rule(self):
        """Test that position_rotation_encouraged is defined."""
        config = load_sport_config("baseball")

        assert "position_rotation_encouraged" in config.rules.generation_rules
        assert config.rules.generation_rules["position_rotation_encouraged"] is True

    def test_baseball_generator_reads_pitcher_rule(self):
        """Test that BaseballLineupGenerator reads pitcher_max_innings from config."""
        from sports.generators.baseball import BaseballLineupGenerator

        config = load_sport_config("baseball")
        generator = BaseballLineupGenerator(config)

        assert generator.pitcher_max_innings == 2


class TestVolleyballGenerationRules:
    """Tests for volleyball generation rules."""

    def test_volleyball_config_has_generation_rules(self):
        """Test that volleyball config includes generation_rules."""
        config = load_sport_config("volleyball")

        assert hasattr(config.rules, "generation_rules")
        assert config.rules.generation_rules is not None
        assert isinstance(config.rules.generation_rules, dict)

    def test_volleyball_rotation_required_rule(self):
        """Test that rotation_required is defined."""
        config = load_sport_config("volleyball")

        assert "rotation_required" in config.rules.generation_rules
        assert config.rules.generation_rules["rotation_required"] is True

    def test_volleyball_min_players_rule(self):
        """Test that min_players_required is defined."""
        config = load_sport_config("volleyball")

        assert "min_players_required" in config.rules.generation_rules
        assert config.rules.generation_rules["min_players_required"] == 6

    def test_volleyball_libero_restrictions_rule(self):
        """Test that libero_restrictions is defined."""
        config = load_sport_config("volleyball")

        assert "libero_restrictions" in config.rules.generation_rules
        assert config.rules.generation_rules["libero_restrictions"] is False

    def test_volleyball_generator_reads_rotation_rule(self):
        """Test that VolleyballLineupGenerator reads rotation_required from config."""
        from sports.generators.volleyball import VolleyballLineupGenerator

        config = load_sport_config("volleyball")
        generator = VolleyballLineupGenerator(config)

        assert generator.rotation_required is True

    def test_volleyball_generator_reads_libero_rule(self):
        """Test that VolleyballLineupGenerator reads libero_restrictions from config."""
        from sports.generators.volleyball import VolleyballLineupGenerator

        config = load_sport_config("volleyball")
        generator = VolleyballLineupGenerator(config)

        assert generator.libero_restrictions is False


class TestSoccerGenerationRules:
    """Tests for soccer generation rules."""

    def test_soccer_config_has_generation_rules(self):
        """Test that soccer config includes generation_rules."""
        config = load_sport_config("soccer")

        assert hasattr(config.rules, "generation_rules")
        assert config.rules.generation_rules is not None
        assert isinstance(config.rules.generation_rules, dict)

    def test_soccer_substitution_limit_rule(self):
        """Test that substitution_limit is defined."""
        config = load_sport_config("soccer")

        assert "substitution_limit" in config.rules.generation_rules
        assert config.rules.generation_rules["substitution_limit"] == 3

    def test_soccer_goalkeeper_required_rule(self):
        """Test that goalkeeper_required is defined."""
        config = load_sport_config("soccer")

        assert "goalkeeper_required" in config.rules.generation_rules
        assert config.rules.generation_rules["goalkeeper_required"] is True

    def test_soccer_min_players_rule(self):
        """Test that min_players_required is defined."""
        config = load_sport_config("soccer")

        assert "min_players_required" in config.rules.generation_rules
        assert config.rules.generation_rules["min_players_required"] == 11


class TestGenerationRulesDefaults:
    """Tests for generation rules default handling."""

    def test_missing_generation_rules_defaults_to_empty_dict(self):
        """Test that missing generation_rules defaults to empty dict."""
        from sports.models.sport_config import SportRules

        rules = SportRules(total_positions=9)

        assert rules.generation_rules == {}

    def test_generator_handles_missing_pitcher_rule(self):
        """Test that BaseballLineupGenerator handles missing pitcher rule gracefully."""
        from sports.generators.baseball import BaseballLineupGenerator
        from sports.models.sport_config import (
            FieldDiagram,
            GameStructure,
            SportConfig,
            SportRules,
        )

        # Create config without pitcher_max_consecutive_innings
        config = SportConfig(
            sport_id="baseball",
            display_name="Baseball",
            positions=[],
            game_structure=GameStructure(
                type="innings", periods=6, period_name="Inning"
            ),
            rules=SportRules(total_positions=9, generation_rules={}),  # Empty rules
            field_diagram=FieldDiagram(
                type="diamond", width=800, height=800, position_coordinates={}
            ),
        )

        generator = BaseballLineupGenerator(config)

        # Should default to 2
        assert generator.pitcher_max_innings == 2

    def test_generator_handles_missing_volleyball_rules(self):
        """Test that VolleyballLineupGenerator handles missing rules gracefully."""
        from sports.generators.volleyball import VolleyballLineupGenerator
        from sports.models.sport_config import (
            FieldDiagram,
            GameStructure,
            SportConfig,
            SportRules,
        )

        # Create config without rotation rules
        config = SportConfig(
            sport_id="volleyball",
            display_name="Volleyball",
            positions=[],
            game_structure=GameStructure(type="sets", periods=3, period_name="Set"),
            rules=SportRules(total_positions=6, generation_rules={}),  # Empty rules
            field_diagram=FieldDiagram(
                type="court", width=600, height=400, position_coordinates={}
            ),
        )

        generator = VolleyballLineupGenerator(config)

        # Should default to True and False
        assert generator.rotation_required is True
        assert generator.libero_restrictions is False
