"""
Tests for TeamSnap API integration routes with comprehensive mocking
"""

import os
import sys
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

import pytest

# Add the parent directory to sys.path
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


class TestTeamSnapGamesIntegration:
    """Tests for TeamSnap /api/games route with mocked responses"""

    @patch("app.requests.get")
    def test_get_games_with_include_all_states(self, mock_get, authenticated_session):
        """Test /api/games with include_all_states=true"""
        # Mock the events search response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "collection": {
                "items": [
                    {
                        "data": [
                            {"name": "id", "value": "event1"},
                            {"name": "name", "value": "vs Blue Jays"},
                            {"name": "starts_at", "value": "2024-06-15T14:00:00Z"},
                            {"name": "location_name", "value": "City Stadium"},
                        ]
                    }
                ]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        response = authenticated_session.get(
            "/api/games/team123?include_all_states=true"
        )

        assert response.status_code == 200
        data = response.get_json()
        assert "games" in data
        # Verify the API was called with correct URL
        assert mock_get.called
        call_url = mock_get.call_args[0][0]
        assert "include_all_states=true" not in call_url  # We don't pass this to API

    @patch("app.requests.get")
    def test_get_games_without_include_all_states(
        self, mock_get, authenticated_session
    ):
        """Test /api/games with default state filtering"""
        # Mock the events search response with date filtering
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "collection": {
                "items": [
                    {
                        "data": [
                            {"name": "id", "value": "event2"},
                            {"name": "name", "value": "vs Cardinals"},
                            {"name": "starts_at", "value": "2024-06-20T18:30:00Z"},
                            {"name": "location_name", "value": "Home Field"},
                        ]
                    }
                ]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        response = authenticated_session.get("/api/games/team456")

        assert response.status_code == 200
        data = response.get_json()
        assert "games" in data

    @patch("app.requests.get")
    def test_get_games_with_empty_results(self, mock_get, authenticated_session):
        """Test /api/games when no games are returned"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"collection": {"items": []}}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        response = authenticated_session.get("/api/games/team789")

        assert response.status_code == 200
        data = response.get_json()
        assert "games" in data
        assert len(data["games"]) == 0

    @patch("app.requests.get")
    def test_get_games_with_missing_location(self, mock_get, authenticated_session):
        """Test /api/games when location_name is missing"""
        from datetime import datetime, timedelta, timezone

        # Create a future date for the game
        future_date = (datetime.now(timezone.utc) + timedelta(days=7)).isoformat()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            "collection": {
                "items": [
                    {
                        "data": [
                            {"name": "id", "value": "event3"},
                            {"name": "name", "value": "vs Rangers"},
                            {
                                "name": "is_game",
                                "value": True,
                            },  # Must be marked as game
                            {"name": "start_date", "value": future_date},
                            # No location_name field
                        ]
                    }
                ]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        response = authenticated_session.get("/api/games/team999")

        assert response.status_code == 200
        data = response.get_json()
        assert "games" in data
        assert len(data["games"]) == 1
        assert data["games"][0]["location"] == "TBD"

    @patch("app.requests.get")
    def test_get_games_request_exception(self, mock_get, authenticated_session):
        """Test /api/games handles request exceptions"""
        from requests.exceptions import RequestException

        mock_get.side_effect = RequestException("Network timeout")

        response = authenticated_session.get("/api/games/team111")

        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data


class TestTeamSnapAvailabilityIntegration:
    """Tests for TeamSnap /api/availability route with mocked responses"""

    @patch("app.requests.get")
    def test_get_availability_success(self, mock_get, authenticated_session):
        """Test /api/availability with successful response"""
        # Mock availability response
        mock_avail_response = MagicMock()
        mock_avail_response.json.return_value = {
            "collection": {
                "items": [
                    {
                        "data": [
                            {"name": "member_id", "value": "member1"},
                            {"name": "status_code", "value": 1},  # Available
                        ]
                    }
                ]
            }
        }
        mock_avail_response.raise_for_status = MagicMock()

        # Mock member details response
        mock_member_response = MagicMock()
        mock_member_response.status_code = 200
        mock_member_response.json.return_value = {
            "collection": {
                "items": [
                    {
                        "data": [
                            {"name": "id", "value": "member1"},
                            {"name": "first_name", "value": "John"},
                            {"name": "last_name", "value": "Doe"},
                            {"name": "is_non_player", "value": False},
                        ]
                    }
                ]
            }
        }
        mock_member_response.raise_for_status = MagicMock()

        # Return different responses for availability and member calls
        mock_get.side_effect = [mock_avail_response, mock_member_response]

        response = authenticated_session.get("/api/availability/event123")

        assert response.status_code == 200
        data = response.get_json()
        assert "attending_players" in data

    @patch("app.requests.get")
    def test_get_availability_empty_results(self, mock_get, authenticated_session):
        """Test /api/availability with no availability data"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"collection": {"items": []}}
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        response = authenticated_session.get("/api/availability/event456")

        assert response.status_code == 200
        data = response.get_json()
        assert "attending_players" in data
        assert len(data["attending_players"]) == 0

    @patch("app.requests.get")
    def test_get_availability_request_exception(self, mock_get, authenticated_session):
        """Test /api/availability handles request exceptions"""
        from requests.exceptions import RequestException

        mock_get.side_effect = RequestException("API timeout")

        response = authenticated_session.get("/api/availability/event789")

        assert response.status_code == 500
        data = response.get_json()
        assert "error" in data

    def test_get_availability_not_authenticated(self, client):
        """Test /api/availability without authentication"""
        response = client.get("/api/availability/event999")

        assert response.status_code == 401
        data = response.get_json()
        assert "error" in data
