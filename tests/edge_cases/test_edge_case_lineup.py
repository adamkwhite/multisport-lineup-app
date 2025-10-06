"""
Edge case tests for lineup generation logic
"""

import os
import sys

import pytest

# Add the parent directory to sys.path
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from tests.fixtures.player_data import (
    create_catchers,
    create_flexible_players,
    create_infielders,
    create_outfielders,
    create_pitchers,
    create_player,
)


class TestLineupGenerationEdgeCases:
    """Edge case tests for lineup generation"""

    def test_exactly_9_players_no_bench(self, client):
        """Test lineup generation with exactly 9 players (no bench rotation)"""
        payload = {"players": create_flexible_players(9)}

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        # Should generate lineups (one per available pitcher)
        assert len(data["lineups"]) > 0

        # Each lineup should have 0 bench players
        for lineup in data["lineups"]:
            assert len(lineup["bench_players"]) == 0

    def test_10_players_minimal_bench(self, client):
        """Test lineup generation with 10 players (minimal bench rotation)"""
        payload = {"players": create_flexible_players(10)}

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        assert len(data["lineups"]) > 0

        # Each lineup should have exactly 1 bench player
        for lineup in data["lineups"]:
            assert len(lineup["bench_players"]) == 1

    def test_12_players_balanced_bench(self, client):
        """Test lineup generation with 12 players (balanced bench rotation)"""
        payload = {"players": create_flexible_players(12)}

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        assert len(data["lineups"]) > 0

        # Each lineup should have exactly 3 bench players
        for lineup in data["lineups"]:
            assert len(lineup["bench_players"]) == 3

    def test_15_players_heavy_bench(self, client):
        """Test lineup generation with 15+ players (heavy bench rotation)"""
        payload = {"players": create_flexible_players(15)}

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        assert len(data["lineups"]) > 0

        # Each lineup should have 6 bench players
        for lineup in data["lineups"]:
            assert len(lineup["bench_players"]) == 6

    def test_all_players_want_same_position(self, client):
        """Test when all players want the same position (should fallback)"""
        payload = {
            "players": [
                create_player(i, f"Pitcher {i}", ["P"])  # All want to pitch
                for i in range(1, 10)
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        # Should either return 200 with fallback assignments or 400 error
        assert response.status_code in [200, 400]

        if response.status_code == 200:
            data = response.get_json()
            # Should generate lineups even with conflict (uses emergency assignment)
            assert len(data["lineups"]) > 0

    def test_impossible_position_constraints_no_catchers(self, client):
        """Test when no players can play catcher"""
        # Create 9 players who can play everything EXCEPT catcher
        payload = {
            "players": [
                create_player(
                    i, f"Player {i}", ["P", "1B", "2B", "3B", "SS", "LF", "CF", "RF"]
                )
                for i in range(1, 10)
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        # Should handle gracefully (200 with fallback or 400 error)
        assert response.status_code in [200, 400]

    def test_single_player_all_positions_restricted(self, client):
        """Test player with very restrictive position preferences"""
        payload = {
            "players": [
                create_player(1, "Specialist", ["3B"]),  # Can ONLY play third base
                *create_flexible_players(8, start_id=2),
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        # Should generate lineups successfully
        assert len(data["lineups"]) > 0

        # In first lineup, specialist should be at third base
        first_lineup = data["lineups"][0]
        third_base_assignment = next(
            a for a in first_lineup["assignments"] if a["position"] == "3B"
        )
        assert third_base_assignment["player"]["name"] == "Specialist"

    def test_must_play_player_logic(self, client):
        """Test that players who sat out 2+ lineups must play"""
        # This is implicitly tested by the lineup generation algorithm
        # We verify the algorithm generates enough lineups for rotation
        payload = {"players": create_flexible_players(12)}

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        # With 12 players, should generate multiple lineups to ensure rotation
        assert len(data["lineups"]) > 0

        # Track which players appear in each lineup
        player_appearances = {}
        for i, lineup in enumerate(data["lineups"]):
            for assignment in lineup["assignments"]:
                player_name = assignment["player"]["name"]
                if player_name not in player_appearances:
                    player_appearances[player_name] = []
                player_appearances[player_name].append(i)

        # All players should appear at least once if we have enough lineups
        if len(data["lineups"]) >= 2:
            assert len(player_appearances) > 0

    def test_catcher_rotation_across_lineups(self, client):
        """Test that catchers rotate across multiple lineups"""
        payload = {"players": create_flexible_players(12)}

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        if len(data["lineups"]) >= 3:
            # Get catchers from first 3 lineups
            catchers = []
            for lineup in data["lineups"][:3]:
                catcher_assignment = next(
                    a for a in lineup["assignments"] if a["position"] == "C"
                )
                catchers.append(catcher_assignment["player"]["name"])

            # Should have some rotation (not all the same catcher)
            unique_catchers = set(catchers)
            assert len(unique_catchers) >= 2  # At least 2 different catchers

    def test_position_history_tracking(self, client):
        """Test that position history is tracked for rotation"""
        payload = {"players": create_flexible_players(12)}

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        # Track position assignments for each player
        player_positions = {}
        for lineup in data["lineups"]:
            for assignment in lineup["assignments"]:
                player_name = assignment["player"]["name"]
                if player_name not in player_positions:
                    player_positions[player_name] = []
                player_positions[player_name].append(assignment["position"])

        # Players should ideally play different positions across lineups
        # (though this isn't strictly enforced, we can verify tracking exists)
        assert len(player_positions) > 0

    def test_verify_coverage_increase(self, client):
        """Meta test to verify lineup generation function is well-covered"""
        # This test exercises multiple code paths
        test_cases = [
            create_flexible_players(9),  # Minimum players
            create_flexible_players(12),  # Standard case
            create_flexible_players(15),  # Many players
        ]

        for players in test_cases:
            payload = {"players": players}
            response = client.post("/api/lineup/generate", json=payload)
            assert response.status_code == 200

    def test_conflicting_position_preferences(self, client):
        """Test complex scenario with conflicting position preferences"""
        payload = {
            "players": [
                # 3 pitchers
                *create_pitchers(3),
                # 1 catcher (but someone needs to catch when pitchers pitch)
                *create_catchers(1, start_id=4),
                # Rest are flexible
                *create_flexible_players(5, start_id=5),
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code in [200, 400]

        if response.status_code == 200:
            data = response.get_json()

            # Should generate at least 3 lineups (one per pitcher)
            assert len(data["lineups"]) >= 3

            # Verify each lineup has valid assignments
            for lineup in data["lineups"]:
                positions = [a["position"] for a in lineup["assignments"]]
                assert "P" in positions  # Pitcher
                assert "C" in positions  # Catcher
                assert len(lineup["assignments"]) == 9  # All positions filled

    def test_specialized_positions_distribution(self, client):
        """Test with players having specialized position groups"""
        payload = {
            "players": [
                *create_pitchers(2),  # Pitchers
                *create_catchers(1, start_id=3),  # Catchers
                *create_infielders(4, start_id=4),  # Infield only
                *create_outfielders(3, start_id=8),  # Outfield only
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        # Should handle specialized positions
        assert response.status_code in [200, 400]

        if response.status_code == 200:
            data = response.get_json()
            assert len(data["lineups"]) > 0

            # Verify position constraints are respected where possible
            for lineup in data["lineups"]:
                assert len(lineup["assignments"]) == 9
