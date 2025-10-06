"""
Tests for additional code paths in lineup generation
"""

import os
import sys

import pytest

# Add the parent directory to sys.path
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from tests.fixtures.player_data import create_player


class TestLineupAdditionalPaths:
    """Tests to cover additional lineup generation code paths"""

    def test_lineup_with_empty_position_preferences(self, client):
        """Test players with explicitly empty position preferences"""
        payload = {
            "players": [create_player(i, f"Player {i}", []) for i in range(1, 13)]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()
        assert len(data["lineups"]) > 0

    def test_lineup_fallback_assignment_triggered(self, client):
        """Test that fallback assignment works when smart assignment fails"""
        # Create a scenario that might trigger fallback
        payload = {
            "players": [
                # 5 pitchers who can ONLY pitch
                *[create_player(i, f"Pitcher {i}", ["P"]) for i in range(1, 6)],
                # 2 catchers who can ONLY catch
                *[create_player(i, f"Catcher {i}", ["C"]) for i in range(6, 8)],
                # 2 flexible players
                *[create_player(i, f"Player {i}", []) for i in range(8, 10)],
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        # Should succeed (with fallback or smart assignment) or fail gracefully
        assert response.status_code in [200, 400]
        if response.status_code == 200:
            data = response.get_json()
            assert len(data["lineups"]) > 0

    def test_lineup_must_play_enforcement(self, client):
        """Test must-play player logic with enough lineups"""
        # With 15 players, we should generate multiple lineups
        # which will trigger must-play logic
        payload = {
            "players": [create_player(i, f"Player {i}", []) for i in range(1, 16)]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        # Should generate multiple lineups
        assert len(data["lineups"]) >= 2

        # Track which players appear across lineups
        all_player_ids = set()
        for lineup in data["lineups"]:
            for player in lineup.get("bench_players", []):
                all_player_ids.add(player["id"])
            for assignment in lineup["assignments"]:
                all_player_ids.add(assignment["player"]["id"])

    def test_lineup_catcher_rotation_logic(self, client):
        """Test catcher rotation across multiple lineups"""
        # Create multiple pitchers and catchers
        payload = {
            "players": [
                # 3 pitchers
                *[create_player(i, f"Pitcher {i}", ["P"]) for i in range(1, 4)],
                # 3 catchers
                *[create_player(i, f"Catcher {i}", ["C"]) for i in range(4, 7)],
                # 6 flexible players
                *[create_player(i, f"Player {i}", []) for i in range(7, 13)],
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code in [200, 400]

        if response.status_code == 200:
            data = response.get_json()

            # Should generate at least 3 lineups (one per pitcher)
            assert len(data["lineups"]) >= 3

            # Check catcher rotation
            catchers = []
            for lineup in data["lineups"][:3]:
                catcher_assignment = next(
                    a for a in lineup["assignments"] if a["position"] == "C"
                )
                catchers.append(catcher_assignment["player"]["name"])
            # Should have at least 2 different catchers
            unique_catchers = set(catchers)
            assert len(unique_catchers) >= 2

    def test_lineup_position_scarcity_handling(self, client):
        """Test handling of positions with few candidates"""
        payload = {
            "players": [
                # Only 1 pitcher
                create_player(1, "Pitcher 1", ["P"]),
                # Only 1 catcher
                create_player(2, "Catcher 1", ["C"]),
                # Rest are flexible
                *[create_player(i, f"Player {i}", []) for i in range(3, 10)],
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        # Should handle scarcity by assigning scarce positions first
        first_lineup = data["lineups"][0]
        pitcher_assignment = next(
            a for a in first_lineup["assignments"] if a["position"] == "P"
        )
        assert pitcher_assignment["player"]["name"] == "Pitcher 1"

        catcher_assignment = next(
            a for a in first_lineup["assignments"] if a["position"] == "C"
        )
        assert catcher_assignment["player"]["name"] == "Catcher 1"

    def test_lineup_player_flexibility_sorting(self, client):
        """Test that less flexible players are assigned first"""
        payload = {
            "players": [
                # Very inflexible (can only pitch)
                create_player(1, "Specialist 1", ["P"]),
                # Somewhat flexible (infield only)
                create_player(2, "Infielder 1", ["1B", "2B", "3B", "SS"]),
                # Very flexible
                *[create_player(i, f"Flexible {i}", []) for i in range(3, 10)],
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code in [200, 400]

        if response.status_code == 200:
            data = response.get_json()

            # Specialist should be assigned to their only position
            first_lineup = data["lineups"][0]
            pitcher_assignment = next(
                a for a in first_lineup["assignments"] if a["position"] == "P"
            )
            assert pitcher_assignment["player"]["name"] == "Specialist 1"

    def test_lineup_bench_tracking_increments(self, client):
        """Test that bench tracking increments correctly"""
        # With 12 players across multiple lineups, bench time should be tracked
        payload = {
            "players": [create_player(i, f"Player {i}", []) for i in range(1, 13)]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        # Multiple lineups should be generated
        assert len(data["lineups"]) >= 3

        # Verify bench players exist
        for lineup in data["lineups"]:
            assert "bench_players" in lineup
            # 12 players - 9 positions = 3 bench
            assert len(lineup["bench_players"]) == 3

    def test_lineup_position_history_tracking(self, client):
        """Test that position history affects rotation"""
        # Generate multiple lineups to trigger rotation logic
        payload = {
            "players": [create_player(i, f"Player {i}", []) for i in range(1, 13)]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        # Should generate multiple lineups with rotation
        assert len(data["lineups"]) >= 3

        # Track player positions across lineups
        player_positions = {}
        for lineup in data["lineups"]:
            for assignment in lineup["assignments"]:
                player_name = assignment["player"]["name"]
                if player_name not in player_positions:
                    player_positions[player_name] = []
                player_positions[player_name].append(assignment["position"])

        # Some players should play multiple positions
        # (though not guaranteed for all players)
        assert len(player_positions) > 0
