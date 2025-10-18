"""
Tests for authentication routes
"""

import os
import sys
from unittest.mock import MagicMock, patch

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


class TestAuthRoutes:
    """Tests for authentication routes"""

    def test_index_without_auth(self, client):
        """Test that index shows login page when not authenticated"""
        response = client.get("/")
        assert response.status_code == 200
        # Should show login page
        assert (
            b"TeamSnap" in response.data
            or b"Login" in response.data
            or b"Demo" in response.data
        )

    def test_index_with_auth(self, client):
        """Test that index shows dashboard when authenticated"""
        with client.session_transaction() as sess:
            sess["access_token"] = "fake_token"

        response = client.get("/")
        assert response.status_code == 200

    def test_login_route(self, client):
        """Test that /auth/login redirects to TeamSnap"""
        response = client.get("/auth/login", follow_redirects=False)
        assert response.status_code == 302
        assert "auth.teamsnap.com" in response.location
        assert "oauth/authorize" in response.location
        assert "client_id" in response.location

    def test_auth_callback_without_code(self, client):
        """Test auth callback fails without code parameter"""
        response = client.get("/auth/callback")
        assert response.status_code == 400
        assert b"Authentication failed" in response.data

    @patch("app.requests.post")
    def test_auth_callback_success(self, mock_post, client):
        """Test successful auth callback"""
        # Mock the token exchange response
        mock_response = MagicMock()
        mock_response.json.return_value = {"access_token": "test_token_123"}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        response = client.get("/auth/callback?code=test_code", follow_redirects=False)

        assert response.status_code == 302
        # Now redirects to /baseball by default (not /)
        assert response.location.endswith("/baseball")

        # Check that token was stored in session
        with client.session_transaction() as sess:
            assert sess.get("access_token") == "test_token_123"

    @patch("app.requests.post")
    def test_auth_callback_token_exchange_failure(self, mock_post, client):
        """Test auth callback handles token exchange failure"""
        # Mock a failed token exchange with requests.RequestException
        from requests.exceptions import RequestException

        mock_post.side_effect = RequestException("Token exchange failed")

        response = client.get("/auth/callback?code=test_code")

        assert response.status_code == 400
        assert b"Token exchange failed" in response.data

    def test_logout(self, client):
        """Test logout clears session"""
        # Set up a session
        with client.session_transaction() as sess:
            sess["access_token"] = "fake_token"
            sess["demo_mode"] = True

        # Logout
        response = client.get("/logout", follow_redirects=False)

        assert response.status_code == 302
        assert response.location.endswith("/")

        # Check session is cleared
        with client.session_transaction() as sess:
            assert "access_token" not in sess
            assert "demo_mode" not in sess

    def test_api_teams_requires_auth(self, client):
        """Test that /api/teams requires authentication"""
        response = client.get("/api/teams")
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
        assert "Not authenticated" in data["error"]

    def test_api_games_requires_auth(self, client):
        """Test that /api/games requires authentication"""
        response = client.get("/api/games/some-team-id")
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data

    def test_api_availability_requires_auth(self, client):
        """Test that /api/availability requires authentication"""
        response = client.get("/api/availability/some-event-id")
        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
