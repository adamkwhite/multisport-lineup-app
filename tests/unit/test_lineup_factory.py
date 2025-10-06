"""
Unit tests for lineup generator factory.

Tests the factory function that creates sport-specific lineup generators.
"""

import pytest

from sports.generators.base import LineupGenerator
from sports.generators.baseball import BaseballLineupGenerator
from sports.services.lineup_factory import (
    get_lineup_generator,
    get_supported_sports,
    is_sport_supported,
)


class TestGetLineupGenerator:
    """Tests for get_lineup_generator factory function."""

    def test_returns_baseball_generator(self):
        """Test that 'baseball' returns BaseballLineupGenerator."""
        generator = get_lineup_generator("baseball")

        assert isinstance(generator, BaseballLineupGenerator)
        assert isinstance(generator, LineupGenerator)

    def test_baseball_case_insensitive(self):
        """Test that sport_id is case-insensitive."""
        # All should work
        assert isinstance(get_lineup_generator("baseball"), BaseballLineupGenerator)
        assert isinstance(get_lineup_generator("Baseball"), BaseballLineupGenerator)
        assert isinstance(get_lineup_generator("BASEBALL"), BaseballLineupGenerator)
        assert isinstance(get_lineup_generator("BaSeBaLl"), BaseballLineupGenerator)

    def test_baseball_strips_whitespace(self):
        """Test that whitespace is stripped from sport_id."""
        assert isinstance(get_lineup_generator(" baseball "), BaseballLineupGenerator)
        assert isinstance(get_lineup_generator("baseball\n"), BaseballLineupGenerator)
        assert isinstance(get_lineup_generator("\tbaseball"), BaseballLineupGenerator)

    def test_generator_has_config(self):
        """Test that returned generator has valid configuration."""
        generator = get_lineup_generator("baseball")

        assert generator.config is not None
        assert generator.config.sport_id == "baseball"
        assert len(generator.config.positions) == 9  # Baseball has 9 positions

    def test_unknown_sport_raises_error(self):
        """Test that unknown sport raises ValueError."""
        with pytest.raises(ValueError, match="Unknown sport: 'football'"):
            get_lineup_generator("football")

    def test_empty_sport_id_raises_error(self):
        """Test that empty sport_id raises ValueError."""
        with pytest.raises(ValueError, match="sport_id is required"):
            get_lineup_generator("")

    def test_none_sport_id_raises_error(self):
        """Test that None sport_id raises ValueError."""
        with pytest.raises(ValueError, match="sport_id is required"):
            get_lineup_generator(None)

    def test_invalid_type_raises_error(self):
        """Test that non-string sport_id raises ValueError."""
        with pytest.raises(ValueError, match="sport_id must be a string"):
            get_lineup_generator(123)

        with pytest.raises(ValueError, match="sport_id must be a string"):
            get_lineup_generator(["baseball"])

    def test_soccer_not_implemented(self):
        """Test that soccer raises NotImplementedError."""
        with pytest.raises(NotImplementedError, match="Soccer lineup generation"):
            get_lineup_generator("soccer")

    def test_volleyball_not_implemented(self):
        """Test that volleyball raises NotImplementedError."""
        with pytest.raises(NotImplementedError, match="Volleyball lineup generation"):
            get_lineup_generator("volleyball")

    def test_generator_is_usable(self):
        """Test that returned generator can actually generate lineups."""
        from sports.models.lineup import Player

        generator = get_lineup_generator("baseball")

        # Create minimal test data
        players = [
            Player(id=str(i), name=f"Player {i}", position_preferences=[])
            for i in range(1, 13)
        ]
        game_info = {"game_id": "test", "team_id": "test"}

        # Should not raise
        lineups = generator.generate(players, game_info)

        assert len(lineups) == 3  # Baseball generates 3 periods
        assert all(len(lineup.assignments) == 9 for lineup in lineups)


class TestGetSupportedSports:
    """Tests for get_supported_sports helper function."""

    def test_returns_list(self):
        """Test that function returns a list."""
        sports = get_supported_sports()
        assert isinstance(sports, list)

    def test_contains_baseball(self):
        """Test that baseball is in supported sports."""
        sports = get_supported_sports()
        assert "baseball" in sports

    def test_does_not_contain_unimplemented_sports(self):
        """Test that unimplemented sports are not included."""
        sports = get_supported_sports()
        assert "soccer" not in sports
        assert "volleyball" not in sports


class TestIsSportSupported:
    """Tests for is_sport_supported helper function."""

    def test_baseball_is_supported(self):
        """Test that baseball is recognized as supported."""
        assert is_sport_supported("baseball") is True

    def test_baseball_case_insensitive(self):
        """Test that check is case-insensitive."""
        assert is_sport_supported("Baseball") is True
        assert is_sport_supported("BASEBALL") is True

    def test_baseball_strips_whitespace(self):
        """Test that whitespace is stripped."""
        assert is_sport_supported(" baseball ") is True

    def test_soccer_not_supported(self):
        """Test that soccer is not yet supported."""
        assert is_sport_supported("soccer") is False

    def test_volleyball_not_supported(self):
        """Test that volleyball is not yet supported."""
        assert is_sport_supported("volleyball") is False

    def test_unknown_sport_not_supported(self):
        """Test that unknown sports return False."""
        assert is_sport_supported("football") is False
        assert is_sport_supported("basketball") is False

    def test_empty_string_not_supported(self):
        """Test that empty string returns False."""
        assert is_sport_supported("") is False

    def test_none_not_supported(self):
        """Test that None returns False."""
        assert is_sport_supported(None) is False

    def test_invalid_type_not_supported(self):
        """Test that non-string types return False."""
        assert is_sport_supported(123) is False
        assert is_sport_supported(["baseball"]) is False


class TestFactoryIntegration:
    """Integration tests for the factory pattern."""

    def test_multiple_generators_independent(self):
        """Test that multiple generator instances are independent."""
        gen1 = get_lineup_generator("baseball")
        gen2 = get_lineup_generator("baseball")

        # Different instances
        assert gen1 is not gen2

        # But same type
        assert type(gen1) == type(gen2)

    def test_generator_inheritance_chain(self):
        """Test that generators properly inherit from base class."""
        generator = get_lineup_generator("baseball")

        # Check inheritance chain
        assert isinstance(generator, LineupGenerator)
        assert isinstance(generator, BaseballLineupGenerator)

        # Has abstract methods implemented
        assert hasattr(generator, "generate")
        assert callable(generator.generate)
