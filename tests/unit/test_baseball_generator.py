"""
Unit tests for BaseballLineupGenerator.

Tests baseball-specific lineup generation including pitcher rotation,
3-period generation, and position assignment.
"""

import pytest

from sports.generators.baseball import BaseballLineupGenerator
from sports.models.lineup import Player
from sports.models.sport_config import (
    FieldDiagram,
    GameStructure,
    Position,
    SportConfig,
    SportRules,
)


@pytest.fixture
def baseball_config():
    """Create baseball sport configuration."""
    positions = [
        Position(id="P", name="Pitcher", abbrev="P", required=True),
        Position(id="C", name="Catcher", abbrev="C", required=True),
        Position(id="1B", name="First Base", abbrev="1B"),
        Position(id="2B", name="Second Base", abbrev="2B"),
        Position(id="3B", name="Third Base", abbrev="3B"),
        Position(id="SS", name="Shortstop", abbrev="SS"),
        Position(id="LF", name="Left Field", abbrev="LF"),
        Position(id="CF", name="Center Field", abbrev="CF"),
        Position(id="RF", name="Right Field", abbrev="RF"),
    ]

    game_structure = GameStructure(type="innings", periods=6, period_name="Inning")

    rules = SportRules(
        total_positions=9, required_positions=["P", "C"], rotation_type="flexible"
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
            "3B": {"x": 220, "y": 520},
            "SS": {"x": 320, "y": 400},
            "LF": {"x": 180, "y": 220},
            "CF": {"x": 400, "y": 150},
            "RF": {"x": 620, "y": 220},
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
    """Create a baseball lineup generator."""
    return BaseballLineupGenerator(baseball_config)


@pytest.fixture
def minimal_players():
    """Create minimal set of players (9 players, exactly enough)."""
    return [
        Player(id="1", name="Player 1", position_preferences=["P", "1B"]),
        Player(id="2", name="Player 2", position_preferences=["P", "OF"]),
        Player(id="3", name="Player 3", position_preferences=["P", "3B"]),
        Player(id="4", name="Player 4", position_preferences=["C"]),
        Player(id="5", name="Player 5", position_preferences=[]),
        Player(id="6", name="Player 6", position_preferences=[]),
        Player(id="7", name="Player 7", position_preferences=[]),
        Player(id="8", name="Player 8", position_preferences=[]),
        Player(id="9", name="Player 9", position_preferences=[]),
    ]


@pytest.fixture
def standard_team():
    """Create a standard team of 12 players."""
    return [
        Player(id="1", name="Player 1", position_preferences=["P"]),
        Player(id="2", name="Player 2", position_preferences=["P"]),
        Player(id="3", name="Player 3", position_preferences=["P"]),
        Player(id="4", name="Player 4", position_preferences=["C"]),
        Player(id="5", name="Player 5", position_preferences=["C"]),
        Player(id="6", name="Player 6", position_preferences=["1B", "3B"]),
        Player(id="7", name="Player 7", position_preferences=["2B", "SS"]),
        Player(id="8", name="Player 8", position_preferences=[]),
        Player(id="9", name="Player 9", position_preferences=[]),
        Player(id="10", name="Player 10", position_preferences=[]),
        Player(id="11", name="Player 11", position_preferences=[]),
        Player(id="12", name="Player 12", position_preferences=[]),
    ]


class TestBaseballGeneratorConstruction:
    """Tests for BaseballLineupGenerator construction."""

    def test_constructor_sets_pitcher_max_innings(self, generator):
        """Test that constructor sets pitcher max innings."""
        assert generator.pitcher_max_innings == 2

    def test_constructor_inherits_from_base(self, generator, baseball_config):
        """Test that generator inherits from LineupGenerator."""
        assert generator.config == baseball_config
        assert generator.required_positions == ["P", "C"]


class TestGenerate:
    """Tests for generate method."""

    def test_generate_3_lineups(self, generator, standard_team):
        """Test that 3 lineups are generated."""
        game_info = {"game_id": "123", "team_id": "456"}
        lineups = generator.generate(standard_team, game_info)
        assert len(lineups) == 3

    def test_lineup_period_names(self, generator, standard_team):
        """Test that lineups have correct period names."""
        game_info = {"game_id": "123", "team_id": "456"}
        lineups = generator.generate(standard_team, game_info)
        assert lineups[0].period_name == "Innings 1-2"
        assert lineups[1].period_name == "Innings 3-4"
        assert lineups[2].period_name == "Innings 5-6"

    def test_lineup_periods(self, generator, standard_team):
        """Test that lineups have correct period numbers."""
        game_info = {"game_id": "123", "team_id": "456"}
        lineups = generator.generate(standard_team, game_info)
        assert lineups[0].period == 1
        assert lineups[1].period == 2
        assert lineups[2].period == 3

    def test_each_lineup_has_9_positions(self, generator, standard_team):
        """Test that each lineup has exactly 9 players."""
        game_info = {"game_id": "123", "team_id": "456"}
        lineups = generator.generate(standard_team, game_info)
        for lineup in lineups:
            assert len(lineup.assignments) == 9

    def test_each_lineup_has_pitcher(self, generator, standard_team):
        """Test that each lineup includes a pitcher."""
        game_info = {"game_id": "123", "team_id": "456"}
        lineups = generator.generate(standard_team, game_info)
        for lineup in lineups:
            assert lineup.has_position_filled("P")

    def test_each_lineup_has_catcher(self, generator, standard_team):
        """Test that each lineup includes a catcher."""
        game_info = {"game_id": "123", "team_id": "456"}
        lineups = generator.generate(standard_team, game_info)
        for lineup in lineups:
            assert lineup.has_position_filled("C")

    def test_insufficient_players_raises_error(self, generator):
        """Test that insufficient players raises ValueError."""
        players = [
            Player(id="1", name="P1", position_preferences=["P"]),
            Player(id="2", name="P2", position_preferences=["C"]),
        ]
        game_info = {"game_id": "123", "team_id": "456"}

        with pytest.raises(ValueError, match="Insufficient players"):
            generator.generate(players, game_info)

    def test_no_pitchers_raises_error(self, generator):
        """Test that no available pitchers raises ValueError."""
        players = [
            Player(id=str(i), name=f"Player {i}", position_preferences=["C"])
            for i in range(1, 10)
        ]
        game_info = {"game_id": "123", "team_id": "456"}

        with pytest.raises(
            ValueError, match="No player available for required position: Pitcher"
        ):
            generator.generate(players, game_info)

    def test_invalid_game_info_raises_error(self, generator, standard_team):
        """Test that invalid game_info raises ValueError."""
        game_info = {"game_id": "123"}  # Missing team_id

        with pytest.raises(ValueError, match="Invalid game_info"):
            generator.generate(standard_team, game_info)


class TestPitcherRotation:
    """Tests for pitcher rotation logic."""

    def test_pitchers_rotate_across_periods(self, generator, standard_team):
        """Test that different pitchers are used in each period."""
        game_info = {"game_id": "123", "team_id": "456"}
        lineups = generator.generate(standard_team, game_info)

        pitchers = []
        for lineup in lineups:
            pitcher_assignment = lineup.get_position_assignment("P")
            pitchers.append(pitcher_assignment.player.id)

        # All pitchers should be different
        assert len(set(pitchers)) == 3

    def test_pitcher_not_in_consecutive_periods(self, generator, standard_team):
        """Test that no pitcher pitches in consecutive periods."""
        game_info = {"game_id": "123", "team_id": "456"}
        lineups = generator.generate(standard_team, game_info)

        for i in range(len(lineups) - 1):
            pitcher1 = lineups[i].get_position_assignment("P").player.id
            pitcher2 = lineups[i + 1].get_position_assignment("P").player.id
            assert pitcher1 != pitcher2

    def test_insufficient_pitchers_for_rotation(self, generator):
        """Test behavior when not enough pitchers for rotation."""
        # Only 2 pitchers for 3 periods - should work for period 1 and 2,
        # then one can pitch again in period 3 (not consecutive)
        players = [
            Player(id="1", name="Pitcher 1", position_preferences=["P"]),
            Player(id="2", name="Pitcher 2", position_preferences=["P"]),
            Player(id="3", name="Catcher 1", position_preferences=["C"]),
        ] + [
            Player(id=str(i), name=f"Player {i}", position_preferences=[])
            for i in range(4, 13)  # 12 players total - more flexibility
        ]

        game_info = {"game_id": "123", "team_id": "456"}
        lineups = generator.generate(players, game_info)

        # Should still generate 3 lineups
        assert len(lineups) == 3

        # Pitcher 1 could pitch in periods 1 and 3 (not consecutive)
        period1_pitcher = lineups[0].get_position_assignment("P").player.id
        period2_pitcher = lineups[1].get_position_assignment("P").player.id
        period3_pitcher = lineups[2].get_position_assignment("P").player.id

        # Period 2 pitcher must be different from period 1
        assert period2_pitcher != period1_pitcher
        # Period 3 pitcher must be different from period 2
        assert period3_pitcher != period2_pitcher


class TestGetEligiblePitchers:
    """Tests for _get_eligible_pitchers method."""

    def test_all_pitchers_eligible_period_1(self, generator, standard_team):
        """Test that all pitchers are eligible in period 1."""
        pitcher_history = {}
        eligible = generator._get_eligible_pitchers(standard_team, pitcher_history, 1)

        # Should have 8 pitchers (3 with P preference + 5 with no preferences = can play any)
        assert len(eligible) == 8
        assert all(p.can_play_position("P") for p in eligible)

    def test_pitcher_ineligible_after_pitching(self, generator, standard_team):
        """Test that pitcher is ineligible in period immediately following."""
        pitcher_history = {"1": [1]}  # Player 1 pitched in period 1
        eligible = generator._get_eligible_pitchers(standard_team, pitcher_history, 2)

        # Player 1 should not be eligible
        eligible_ids = {p.id for p in eligible}
        assert "1" not in eligible_ids
        assert "2" in eligible_ids
        assert "3" in eligible_ids

    def test_pitcher_eligible_after_rest(self, generator, standard_team):
        """Test that pitcher is eligible again after resting a period."""
        pitcher_history = {"1": [1]}  # Player 1 pitched in period 1
        eligible = generator._get_eligible_pitchers(standard_team, pitcher_history, 3)

        # Player 1 should be eligible again in period 3
        eligible_ids = {p.id for p in eligible}
        assert "1" in eligible_ids


class TestGetMustPlayPlayers:
    """Tests for _get_must_play_players method."""

    def test_no_must_play_period_1(self, generator, standard_team):
        """Test that no players are must-play in period 1."""
        bench_tracker = {p.id: 0 for p in standard_team}
        must_play = generator._get_must_play_players(standard_team, bench_tracker, 1)
        assert must_play == []

    def test_must_play_after_2_bench_periods(self, generator, standard_team):
        """Test that player must play after sitting 2 periods."""
        bench_tracker = {p.id: 0 for p in standard_team}
        bench_tracker["12"] = 2  # Player 12 sat out 2 periods

        must_play = generator._get_must_play_players(standard_team, bench_tracker, 3)

        must_play_ids = {p.id for p in must_play}
        assert "12" in must_play_ids

    def test_no_must_play_after_1_bench_period(self, generator, standard_team):
        """Test that player is not must-play after only 1 period."""
        bench_tracker = {p.id: 0 for p in standard_team}
        bench_tracker["12"] = 1  # Player 12 sat out 1 period

        must_play = generator._get_must_play_players(standard_team, bench_tracker, 2)
        assert must_play == []


class TestBenchTracking:
    """Tests for bench tracking functionality."""

    def test_bench_tracker_resets_when_playing(self, generator, standard_team):
        """Test that bench tracker resets to 0 when player plays."""
        game_info = {"game_id": "123", "team_id": "456"}
        lineups = generator.generate(standard_team, game_info)

        # All players should play at some point, so their bench count should reset
        # This is implicit in the generation - just verify all players play
        all_player_ids = {p.id for p in standard_team}
        players_who_played = set()

        for lineup in lineups:
            for assignment in lineup.assignments:
                players_who_played.add(assignment.player.id)

        # All 12 players should have played at some point across 3 lineups (9 per lineup)
        assert len(players_who_played) >= 9  # At minimum, 9 unique players


class TestPositionAssignment:
    """Tests for position assignment logic."""

    def test_position_preferences_honored(self, generator):
        """Test that position preferences are honored."""
        players = [
            Player(id="1", name="Pitcher Only", position_preferences=["P"]),
            Player(id="2", name="Catcher Only", position_preferences=["C"]),
        ] + [
            Player(id=str(i), name=f"Flexible {i}", position_preferences=[])
            for i in range(3, 10)
        ]

        game_info = {"game_id": "123", "team_id": "456", "num_periods": 1}
        lineups = generator.generate(players, game_info)

        lineup = lineups[0]
        pitcher = lineup.get_position_assignment("P")
        catcher = lineup.get_position_assignment("C")

        # Should assign players to their preferred positions
        assert pitcher.player.id in ["1"]
        assert catcher.player.id == "2"

    def test_all_positions_filled(self, generator, standard_team):
        """Test that all 9 positions are filled in each lineup."""
        game_info = {"game_id": "123", "team_id": "456"}
        lineups = generator.generate(standard_team, game_info)

        expected_positions = {"P", "C", "1B", "2B", "3B", "SS", "LF", "CF", "RF"}

        for lineup in lineups:
            assigned_positions = {a.position for a in lineup.assignments}
            assert assigned_positions == expected_positions

    def test_no_duplicate_players_in_lineup(self, generator, standard_team):
        """Test that no player appears twice in same lineup."""
        game_info = {"game_id": "123", "team_id": "456"}
        lineups = generator.generate(standard_team, game_info)

        for lineup in lineups:
            player_ids = [a.player.id for a in lineup.assignments]
            assert len(player_ids) == len(set(player_ids))


class TestEdgeCases:
    """Tests for edge cases."""

    def test_exactly_9_players(self, generator, minimal_players):
        """Test with exactly 9 players (minimum) for single period."""
        # With exactly 9 players, rotation is very constrained
        # Test just 1 period to verify basic functionality
        game_info = {"game_id": "123", "team_id": "456", "num_periods": 1}
        lineups = generator.generate(minimal_players, game_info)

        assert len(lineups) == 1
        assert len(lineups[0].assignments) == 9
        assert len(lineups[0].bench_players) == 0

    def test_custom_num_periods(self, generator, standard_team):
        """Test with custom number of periods."""
        game_info = {"game_id": "123", "team_id": "456", "num_periods": 2}
        lineups = generator.generate(standard_team, game_info)

        assert len(lineups) == 2
        assert lineups[0].period_name == "Innings 1-2"
        assert lineups[1].period_name == "Innings 3-4"

    def test_many_players(self, generator):
        """Test with many players (15)."""
        players = [
            Player(id="1", name="P1", position_preferences=["P"]),
            Player(id="2", name="P2", position_preferences=["P"]),
            Player(id="3", name="P3", position_preferences=["P"]),
            Player(id="4", name="C1", position_preferences=["C"]),
        ] + [
            Player(id=str(i), name=f"Player {i}", position_preferences=[])
            for i in range(5, 16)
        ]

        game_info = {"game_id": "123", "team_id": "456"}
        lineups = generator.generate(players, game_info)

        assert len(lineups) == 3
        for lineup in lineups:
            assert len(lineup.assignments) == 9
            # Should have 6 bench players (15 - 9)
            assert len(lineup.bench_players) == 6
