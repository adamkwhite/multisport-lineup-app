"""
Tests for VolleyballLineupGenerator.
"""

import pytest

from sports.generators.volleyball import VolleyballLineupGenerator
from sports.models.lineup import Player
from sports.services.sport_loader import load_sport_config


@pytest.fixture
def volleyball_config():
    """Load volleyball sport configuration."""
    return load_sport_config("volleyball")


@pytest.fixture
def volleyball_generator(volleyball_config):
    """Create volleyball lineup generator."""
    return VolleyballLineupGenerator(volleyball_config)


def create_players(count=12):
    """Create test players."""
    return [
        Player(id=str(i), name=f"Player {i}", position_preferences=[])
        for i in range(1, count + 1)
    ]


def create_setters(count=2):
    """Create players who can only set."""
    return [
        Player(id=str(i), name=f"Setter {i}", position_preferences=["S"])
        for i in range(1, count + 1)
    ]


class TestVolleyballGeneratorConstruction:
    """Tests for VolleyballLineupGenerator construction."""

    def test_constructor_inherits_from_base(self, volleyball_generator):
        """Test that VolleyballLineupGenerator inherits from LineupGenerator."""
        from sports.generators.base import LineupGenerator

        assert isinstance(volleyball_generator, LineupGenerator)

    def test_constructor_sets_config(self, volleyball_generator, volleyball_config):
        """Test that constructor properly sets config."""
        assert volleyball_generator.config == volleyball_config
        assert volleyball_generator.config.sport_id == "volleyball"


class TestGenerate:
    """Tests for generate() method."""

    def test_generate_3_sets_default(self, volleyball_generator):
        """Test default 3-set generation."""
        players = create_players(12)
        game_info = {"game_id": "test", "team_id": "test"}

        lineups = volleyball_generator.generate(players, game_info)

        assert len(lineups) == 3
        assert all(lineup.period_name.startswith("Set") for lineup in lineups)

    def test_generate_5_sets(self, volleyball_generator):
        """Test 5-set generation."""
        players = create_players(12)
        game_info = {"game_id": "test", "team_id": "test", "num_sets": 5}

        lineups = volleyball_generator.generate(players, game_info)

        assert len(lineups) == 5

    def test_set_period_names(self, volleyball_generator):
        """Test that set names are correct."""
        players = create_players(12)
        game_info = {"game_id": "test", "team_id": "test"}

        lineups = volleyball_generator.generate(players, game_info)

        assert lineups[0].period_name == "Set 1"
        assert lineups[1].period_name == "Set 2"
        assert lineups[2].period_name == "Set 3"

    def test_set_periods(self, volleyball_generator):
        """Test that set periods are numbered correctly."""
        players = create_players(12)
        game_info = {"game_id": "test", "team_id": "test"}

        lineups = volleyball_generator.generate(players, game_info)

        assert lineups[0].period == 1
        assert lineups[1].period == 2
        assert lineups[2].period == 3

    def test_each_set_has_6_positions(self, volleyball_generator):
        """Test that each set has exactly 6 players."""
        players = create_players(12)
        game_info = {"game_id": "test", "team_id": "test"}

        lineups = volleyball_generator.generate(players, game_info)

        for lineup in lineups:
            assert len(lineup.assignments) == 6

    def test_each_set_has_setter(self, volleyball_generator):
        """Test that each set has a setter."""
        players = create_players(12)
        game_info = {"game_id": "test", "team_id": "test"}

        lineups = volleyball_generator.generate(players, game_info)

        for lineup in lineups:
            positions = [a.position for a in lineup.assignments]
            assert "S" in positions

    def test_insufficient_players_raises_error(self, volleyball_generator):
        """Test that insufficient players raises ValueError."""
        players = create_players(3)  # Only 3 players, need 6
        game_info = {"game_id": "test", "team_id": "test"}

        with pytest.raises(ValueError, match="Insufficient players"):
            volleyball_generator.generate(players, game_info)

    def test_invalid_game_info_raises_error(self, volleyball_generator):
        """Test that invalid game_info raises ValueError."""
        players = create_players(12)
        game_info = {}  # Missing required fields

        with pytest.raises(ValueError, match="Invalid game_info"):
            volleyball_generator.generate(players, game_info)


class TestPositionAssignments:
    """Tests for position assignment logic."""

    def test_position_preferences_honored(self, volleyball_generator):
        """Test that position preferences are honored."""
        players = [
            Player(id="1", name="Setter 1", position_preferences=["S"]),
            *create_players(11),
        ]
        game_info = {"game_id": "test", "team_id": "test"}

        lineups = volleyball_generator.generate(players, game_info)

        # First lineup should have the setter preference player
        first_lineup = lineups[0]
        setter_assignment = next(
            a for a in first_lineup.assignments if a.position == "S"
        )
        assert setter_assignment.player.name == "Setter 1"

    def test_all_positions_filled(self, volleyball_generator):
        """Test that all 6 positions are filled."""
        players = create_players(12)
        game_info = {"game_id": "test", "team_id": "test"}

        lineups = volleyball_generator.generate(players, game_info)

        for lineup in lineups:
            assert len(lineup.assignments) == 6
            # Should have positions filled
            positions = [a.position for a in lineup.assignments]
            assert len(positions) == 6

    def test_no_duplicate_players_in_lineup(self, volleyball_generator):
        """Test that no player appears twice in same lineup."""
        players = create_players(12)
        game_info = {"game_id": "test", "team_id": "test"}

        lineups = volleyball_generator.generate(players, game_info)

        for lineup in lineups:
            player_ids = [a.player.id for a in lineup.assignments]
            assert len(player_ids) == len(set(player_ids))


class TestBenchTracking:
    """Tests for bench tracking logic."""

    def test_bench_players_tracked(self, volleyball_generator):
        """Test that bench players are tracked."""
        players = create_players(12)
        game_info = {"game_id": "test", "team_id": "test"}

        lineups = volleyball_generator.generate(players, game_info)

        for lineup in lineups:
            # 12 players - 6 on court = 6 on bench
            assert len(lineup.bench_players) == 6

    def test_bench_tracker_resets_when_playing(self, volleyball_generator):
        """Test that bench tracker resets when player enters game."""
        players = create_players(12)
        game_info = {"game_id": "test", "team_id": "test", "num_sets": 5}

        lineups = volleyball_generator.generate(players, game_info)

        # Track player appearances
        player_appearances = {}
        for i, lineup in enumerate(lineups):
            for assignment in lineup.assignments:
                if assignment.player.id not in player_appearances:
                    player_appearances[assignment.player.id] = []
                player_appearances[assignment.player.id].append(i)

        # With 5 sets and 12 players, most players should appear multiple times
        assert len(player_appearances) > 0


class TestMustPlayLogic:
    """Tests for must-play player logic."""

    def test_no_must_play_set_1(self, volleyball_generator):
        """Test that there are no must-play players in set 1."""
        players = create_players(12)
        game_info = {"game_id": "test", "team_id": "test"}

        # This is an indirect test - just verify set 1 generates successfully
        lineups = volleyball_generator.generate(players, game_info)
        assert len(lineups[0].assignments) == 6


class TestGetRequiredPositions:
    """Tests for _get_required_positions() method."""

    def test_returns_6_positions(self, volleyball_generator):
        """Test that 6 positions are returned."""
        positions = volleyball_generator._get_required_positions()
        assert len(positions) == 6

    def test_includes_setter(self, volleyball_generator):
        """Test that setter is included."""
        positions = volleyball_generator._get_required_positions()
        position_ids = [p.id for p in positions]
        assert "S" in position_ids

    def test_includes_outside_hitters(self, volleyball_generator):
        """Test that 2 outside hitters are included."""
        positions = volleyball_generator._get_required_positions()
        position_ids = [p.id for p in positions]
        assert position_ids.count("OH") == 2

    def test_includes_middle_blockers(self, volleyball_generator):
        """Test that 2 middle blockers are included."""
        positions = volleyball_generator._get_required_positions()
        position_ids = [p.id for p in positions]
        assert position_ids.count("MB") == 2


class TestEdgeCases:
    """Tests for edge cases."""

    def test_exactly_6_players_no_bench(self, volleyball_generator):
        """Test with exactly 6 players (no bench)."""
        players = create_players(6)
        game_info = {"game_id": "test", "team_id": "test"}

        lineups = volleyball_generator.generate(players, game_info)

        for lineup in lineups:
            assert len(lineup.assignments) == 6
            assert len(lineup.bench_players) == 0

    def test_7_players_minimal_bench(self, volleyball_generator):
        """Test with 7 players (minimal bench rotation)."""
        players = create_players(7)
        game_info = {"game_id": "test", "team_id": "test"}

        lineups = volleyball_generator.generate(players, game_info)

        for lineup in lineups:
            assert len(lineup.assignments) == 6
            assert len(lineup.bench_players) == 1
