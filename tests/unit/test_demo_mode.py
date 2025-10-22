"""
Tests for demo mode functionality
"""

import json
import os
import sys

import pytest

# Add the parent directory to sys.path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, load_demo_data


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


class TestDemoMode:
    """Tests for demo mode functionality"""

    def test_demo_route(self, client):
        """Test that /demo route sets up demo mode and redirects to baseball"""
        response = client.get("/demo", follow_redirects=False)
        assert response.status_code == 302  # Redirect
        assert response.location.endswith(
            "/baseball"
        )  # Now redirects to baseball dashboard

        # Check session was set up
        with client.session_transaction() as sess:
            assert sess.get("demo_mode") is True
            assert sess.get("access_token") == "demo_token"

    def test_demo_mode_dashboard_access(self, client):
        """Test that demo mode allows dashboard access"""
        # Set up demo mode
        client.get("/demo")

        # Access baseball dashboard (demo mode should allow access)
        response = client.get("/baseball")
        assert response.status_code == 200

    def test_load_demo_data(self):
        """Test loading demo data from JSON file"""
        data = load_demo_data()

        # Check that demo data loads (if file exists)
        if data is not None:
            assert "team" in data
            assert "players" in data
            assert "games" in data
            assert data["team"]["id"] is not None
            assert len(data["players"]) > 0

    def test_api_teams_demo_mode(self, client):
        """Test /api/teams in demo mode"""
        # Set up demo mode
        client.get("/demo")

        response = client.get("/api/teams")

        # Should return demo team data or error if demo data not available
        assert response.status_code in [200, 500]

        if response.status_code == 200:
            data = response.get_json()
            assert "collection" in data

    def test_api_games_demo_mode(self, client):
        """Test /api/games in demo mode"""
        # Set up demo mode
        client.get("/demo")

        # Need to get the demo team ID first
        demo_data = load_demo_data()
        if demo_data:
            team_id = demo_data["team"]["id"]

            response = client.get(f"/api/games/{team_id}")

            assert response.status_code in [200, 404]

            if response.status_code == 200:
                data = response.get_json()
                assert "games" in data

    def test_api_availability_demo_mode(self, client):
        """Test /api/availability in demo mode"""
        # Set up demo mode
        client.get("/demo")

        demo_data = load_demo_data()
        if demo_data and len(demo_data["games"]) > 0:
            event_id = demo_data["games"][0]["id"]

            response = client.get(f"/api/availability/{event_id}")

            assert response.status_code in [200, 404, 500]

            if response.status_code == 200:
                data = response.get_json()
                assert "attending_players" in data

    def test_load_demo_data_with_sport_parameter(self):
        """Test load_demo_data with explicit sport parameter"""
        # Test baseball demo data
        baseball_data = load_demo_data(sport="baseball")
        assert baseball_data is not None
        assert "team" in baseball_data
        assert "players" in baseball_data
        assert baseball_data["team"]["name"] == "Demo All-Stars"

        # Test volleyball demo data
        volleyball_data = load_demo_data(sport="volleyball")
        assert volleyball_data is not None
        assert "team" in volleyball_data
        assert "players" in volleyball_data
        assert volleyball_data["team"]["name"] == "Demo Volleyball All-Stars"

        # Test that different sports load different data
        assert baseball_data["team"]["id"] != volleyball_data["team"]["id"]

    def test_load_demo_data_volleyball_positions(self):
        """Test volleyball demo data has valid position preferences"""
        data = load_demo_data(sport="volleyball")
        assert data is not None

        valid_positions = ["OH", "MB", "S", "OPP", "L", "DS"]
        position_counts = {pos: 0 for pos in valid_positions}

        for player in data["players"]:
            pos = player["position_preference"]
            assert pos in valid_positions, f"Invalid position: {pos}"
            position_counts[pos] += 1

        # Verify we have at least one player for each position type
        assert position_counts["S"] >= 1, "Should have at least 1 setter"
        assert position_counts["OH"] >= 1, "Should have at least 1 outside hitter"
        assert position_counts["MB"] >= 1, "Should have at least 1 middle blocker"
        assert position_counts["OPP"] >= 1, "Should have at least 1 opposite"
        assert position_counts["L"] >= 1, "Should have at least 1 libero"
        assert position_counts["DS"] >= 1, "Should have at least 1 defensive specialist"

    def test_demo_mode_volleyball_integration(self, client):
        """Test volleyball demo mode end-to-end"""
        # Access volleyball demo mode
        response = client.get("/demo/volleyball", follow_redirects=False)
        assert response.status_code == 302  # Redirect
        assert response.location.endswith("/volleyball")

        # Check session was set up correctly
        with client.session_transaction() as sess:
            assert sess.get("demo_mode") is True
            assert sess.get("access_token") == "demo_token"
            assert sess.get("demo_sport") == "volleyball"

        # Test that API endpoints return volleyball data
        teams_response = client.get("/api/teams")
        if teams_response.status_code == 200:
            teams_data = teams_response.get_json()
            assert "collection" in teams_data
            # The team name should be volleyball team
            team_items = teams_data["collection"]["items"]
            if team_items:
                team_name = next(
                    (
                        item["value"]
                        for item in team_items[0]["data"]
                        if item["name"] == "name"
                    ),
                    None,
                )
                assert team_name == "Demo Volleyball All-Stars"

    def test_demo_mode_without_demo_data_file(self, client, monkeypatch):
        """Test demo mode behavior when demo data file is missing"""

        # Mock load_demo_data to return None
        def mock_load_demo_data():
            return None

        monkeypatch.setattr("app.load_demo_data", mock_load_demo_data)

        # Set up demo mode
        client.get("/demo")

        # Try to get teams - should return error
        response = client.get("/api/teams")
        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data
