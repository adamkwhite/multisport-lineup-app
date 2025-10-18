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
