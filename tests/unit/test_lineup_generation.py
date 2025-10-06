"""
Tests for lineup generation functionality
"""

import os
import sys

import pytest

# Add the parent directory to sys.path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import FIELDING_POSITIONS, app


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


class TestLineupGeneration:
    """Tests for lineup generation endpoint"""

    def test_generate_lineup_insufficient_players(self, client):
        """Test lineup generation with insufficient players"""
        payload = {
            "players": [
                {"id": 1, "name": "Player 1", "position_preferences": []},
                {"id": 2, "name": "Player 2", "position_preferences": []},
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "at least 9 players" in data["error"]

    def test_generate_lineup_no_pitcher(self, client):
        """Test lineup generation with no available pitchers"""
        payload = {
            "players": [
                {
                    "id": i,
                    "name": f"Player {i}",
                    "position_preferences": [
                        "C",
                        "1B",
                        "2B",
                        "3B",
                        "SS",
                        "LF",
                        "CF",
                        "RF",
                    ],
                }
                for i in range(1, 10)
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 400
        data = response.get_json()
        assert "error" in data
        assert "pitch" in data["error"].lower()

    def test_generate_lineup_basic(self, client):
        """Test basic lineup generation with flexible players"""
        payload = {
            "players": [
                {"id": i, "name": f"Player {i}", "position_preferences": []}
                for i in range(1, 10)
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        assert "lineups" in data
        assert "sport" in data
        assert "num_periods" in data
        assert "total_players" in data

        # Should generate lineups based on available pitchers
        assert len(data["lineups"]) > 0
        assert data["sport"] == "baseball"
        assert data["total_players"] == 9

        # Check first lineup structure
        lineup = data["lineups"][0]
        assert "assignments" in lineup
        assert "bench_players" in lineup
        assert "period" in lineup
        assert "period_name" in lineup

        # Check all positions are filled (9 assignments)
        assignments = lineup["assignments"]
        assert len(assignments) == 9
        for assignment in assignments:
            assert "player" in assignment
            assert "position" in assignment
            assert "id" in assignment["player"]
            assert "name" in assignment["player"]

    def test_generate_lineup_with_position_preferences(self, client):
        """Test lineup generation respects position preferences"""
        payload = {
            "players": [
                {"id": 1, "name": "Pitcher Only", "position_preferences": ["P"]},
                {"id": 2, "name": "Catcher Only", "position_preferences": ["C"]},
                {"id": 3, "name": "Player 3", "position_preferences": []},
                {"id": 4, "name": "Player 4", "position_preferences": []},
                {"id": 5, "name": "Player 5", "position_preferences": []},
                {"id": 6, "name": "Player 6", "position_preferences": []},
                {"id": 7, "name": "Player 7", "position_preferences": []},
                {"id": 8, "name": "Player 8", "position_preferences": []},
                {"id": 9, "name": "Player 9", "position_preferences": []},
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        # Should generate multiple lineups (players who can't pitch will pitch in later lineups)
        assert len(data["lineups"]) > 0

        # Check that first lineup has the dedicated pitcher
        lineup = data["lineups"][0]
        pitcher_assignment = next(
            a for a in lineup["assignments"] if a["position"] == "P"
        )
        assert pitcher_assignment["player"]["name"] == "Pitcher Only"

    def test_generate_lineup_with_multiple_pitchers(self, client):
        """Test lineup generation with multiple pitchers"""
        payload = {
            "players": [
                {"id": 1, "name": "Pitcher 1", "position_preferences": ["P"]},
                {"id": 2, "name": "Pitcher 2", "position_preferences": ["P"]},
                {"id": 3, "name": "Pitcher 3", "position_preferences": ["P"]},
                {"id": 4, "name": "Player 4", "position_preferences": []},
                {"id": 5, "name": "Player 5", "position_preferences": []},
                {"id": 6, "name": "Player 6", "position_preferences": []},
                {"id": 7, "name": "Player 7", "position_preferences": []},
                {"id": 8, "name": "Player 8", "position_preferences": []},
                {"id": 9, "name": "Player 9", "position_preferences": []},
                {"id": 10, "name": "Player 10", "position_preferences": []},
                {"id": 11, "name": "Player 11", "position_preferences": []},
                {"id": 12, "name": "Player 12", "position_preferences": []},
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        # Should generate at least 3 lineups (one per dedicated pitcher)
        assert len(data["lineups"]) >= 3

        # Each of the dedicated pitchers should appear as a pitcher in some lineup
        pitchers = []
        for lineup in data["lineups"]:
            pitcher_assignment = next(
                (a for a in lineup["assignments"] if a["position"] == "P"), None
            )
            if pitcher_assignment:
                pitchers.append(pitcher_assignment["player"]["name"])

        assert "Pitcher 1" in pitchers
        assert "Pitcher 2" in pitchers
        assert "Pitcher 3" in pitchers

    def test_generate_lineup_bench_tracking(self, client):
        """Test that players rotate through bench appropriately"""
        # 12 players, 9 positions = 3 bench players per lineup
        payload = {
            "players": [
                {"id": i, "name": f"Player {i}", "position_preferences": []}
                for i in range(1, 13)
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        # Check that bench players are tracked
        for lineup in data["lineups"]:
            assert "bench_players" in lineup
            # 12 players - 9 positions = 3 on bench
            assert len(lineup["bench_players"]) == 3

    def test_generate_lineup_empty_payload(self, client):
        """Test lineup generation with empty payload"""
        response = client.post("/api/lineup/generate", json={})

        assert response.status_code == 400

    def test_generate_lineup_no_json(self, client):
        """Test lineup generation with no JSON payload"""
        response = client.post("/api/lineup/generate")

        # Flask returns 415 or 400 for missing JSON
        assert response.status_code in [400, 415]

    def test_generate_lineup_positions_constant(self, client):
        """Test that position names are correctly returned in assignments"""
        payload = {
            "players": [
                {"id": i, "name": f"Player {i}", "position_preferences": []}
                for i in range(1, 10)
            ]
        }

        response = client.post("/api/lineup/generate", json=payload)

        assert response.status_code == 200
        data = response.get_json()

        # Check position codes are present in lineup assignments
        lineup = data["lineups"][0]
        assignments = lineup["assignments"]

        # Find specific position assignments and verify position codes
        pitcher = next(a for a in assignments if a["position"] == "P")
        assert pitcher["position"] == "P"

        catcher = next(a for a in assignments if a["position"] == "C")
        assert catcher["position"] == "C"

        right_field = next(a for a in assignments if a["position"] == "RF")
        assert right_field["position"] == "RF"
