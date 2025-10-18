"""
Tests for sport-specific routes
"""

import os
import sys

import pytest

# Add the parent directory to sys.path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


class TestSportRoutes:
    """Tests for sport-specific routing"""

    def test_landing_page(self, client):
        """Test that / returns the landing page"""
        response = client.get("/")
        assert response.status_code == 200
        assert b"Multi-Sport Lineup Manager" in response.data
        assert b"Volleyball" in response.data
        assert b"Baseball" in response.data
        assert b"Soccer" in response.data

    def test_baseball_route_without_auth(self, client):
        """Test /baseball redirects to login when not authenticated"""
        response = client.get("/baseball")
        assert response.status_code == 200
        assert b"Baseball Lineup Manager" in response.data
        assert b"Try Demo Mode" in response.data
        # Check sport parameter is passed correctly
        assert b"famous baseball players" in response.data

    def test_baseball_route_with_auth(self, client):
        """Test /baseball shows dashboard when authenticated"""
        # Set up demo mode
        client.get("/demo")

        response = client.get("/baseball")
        assert response.status_code == 200
        assert b"Baseball Lineup Manager" in response.data
        # Should show dashboard, not login screen
        assert b"Try Demo Mode" not in response.data

    def test_volleyball_route_without_auth(self, client):
        """Test /volleyball redirects to login when not authenticated"""
        response = client.get("/volleyball")
        assert response.status_code == 200
        assert b"Volleyball Lineup Manager" in response.data
        assert b"Try Demo Mode" in response.data
        # Check sport parameter is passed correctly
        assert b"famous volleyball players" in response.data

    def test_volleyball_route_with_auth(self, client):
        """Test /volleyball shows dashboard when authenticated"""
        # Set up demo mode
        client.get("/demo")

        response = client.get("/volleyball")
        assert response.status_code == 200
        assert b"Volleyball Lineup Manager" in response.data
        # Should show dashboard, not login screen
        assert b"Try Demo Mode" not in response.data

    def test_soccer_route(self, client):
        """Test /soccer shows coming soon placeholder"""
        response = client.get("/soccer")
        assert response.status_code == 200
        assert b"Soccer Lineup Manager" in response.data
        assert b"Coming Soon" in response.data
        # No auth required for placeholder page

    def test_demo_route_default_sport(self, client):
        """Test /demo defaults to baseball"""
        response = client.get("/demo", follow_redirects=False)
        assert response.status_code == 302
        assert response.location.endswith("/baseball")

    def test_demo_route_with_sport_baseball(self, client):
        """Test /demo/baseball redirects to baseball dashboard"""
        response = client.get("/demo/baseball", follow_redirects=False)
        assert response.status_code == 302
        assert response.location.endswith("/baseball")

    def test_demo_route_with_sport_volleyball(self, client):
        """Test /demo/volleyball redirects to volleyball dashboard"""
        response = client.get("/demo/volleyball", follow_redirects=False)
        assert response.status_code == 302
        assert response.location.endswith("/volleyball")

    def test_demo_route_with_sport_soccer(self, client):
        """Test /demo/soccer redirects to soccer placeholder"""
        response = client.get("/demo/soccer", follow_redirects=False)
        assert response.status_code == 302
        assert response.location.endswith("/soccer")

    def test_demo_route_invalid_sport(self, client):
        """Test /demo with invalid sport defaults to baseball"""
        response = client.get("/demo/invalid", follow_redirects=False)
        assert response.status_code == 302
        assert response.location.endswith("/baseball")
