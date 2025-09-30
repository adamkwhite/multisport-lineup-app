"""
Extended tests for API routes with mocked TeamSnap responses
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestGetTeamsRoute:
    """Extended tests for /api/teams route"""

    @patch('app.requests.get')
    def test_get_teams_with_mocked_response(self, mock_get, authenticated_session):
        """Test /api/teams with mocked TeamSnap response"""
        # Mock the /me endpoint response
        mock_me_response = MagicMock()
        mock_me_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [
                        {'name': 'id', 'value': 'user123'}
                    ],
                    'links': [
                        {'rel': 'teams', 'href': 'https://api.teamsnap.com/v3/teams'}
                    ]
                }]
            }
        }
        mock_me_response.raise_for_status = MagicMock()

        # Mock the /teams endpoint response
        mock_teams_response = MagicMock()
        mock_teams_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [
                        {'name': 'id', 'value': 'team123'},
                        {'name': 'name', 'value': 'Test Team'}
                    ]
                }]
            }
        }
        mock_teams_response.raise_for_status = MagicMock()

        # Configure mock to return different responses for each call
        mock_get.side_effect = [mock_me_response, mock_teams_response]

        response = authenticated_session.get('/api/teams')

        assert response.status_code == 200
        data = response.get_json()
        assert 'collection' in data

    @patch('app.requests.get')
    def test_get_teams_no_teams_url(self, mock_get, authenticated_session):
        """Test /api/teams when no teams URL is found"""
        # Mock the /me endpoint with no teams link and no user_id
        mock_me_response = MagicMock()
        mock_me_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [],
                    'links': []
                }]
            }
        }
        mock_me_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_me_response

        response = authenticated_session.get('/api/teams')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data

    @patch('app.requests.get')
    def test_get_teams_with_user_id_fallback(self, mock_get, authenticated_session):
        """Test /api/teams fallback to user_id search when no teams link"""
        # Mock the /me endpoint with user_id but no teams link
        mock_me_response = MagicMock()
        mock_me_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [
                        {'name': 'id', 'value': 'user456'}
                    ],
                    'links': []  # No teams link
                }]
            }
        }
        mock_me_response.raise_for_status = MagicMock()

        # Mock the teams search response
        mock_teams_response = MagicMock()
        mock_teams_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [
                        {'name': 'id', 'value': 'team789'},
                        {'name': 'name', 'value': 'Fallback Team'}
                    ]
                }]
            }
        }
        mock_teams_response.raise_for_status = MagicMock()

        # Configure mock to return different responses for each call
        mock_get.side_effect = [mock_me_response, mock_teams_response]

        response = authenticated_session.get('/api/teams')

        assert response.status_code == 200
        data = response.get_json()
        assert 'collection' in data


class TestGetGamesRoute:
    """Extended tests for /api/games route"""

    def test_get_games_with_query_params(self, authenticated_session):
        """Test /api/games with include_all_states parameter"""
        response = authenticated_session.get('/api/games/team123?include_all_states=true')

        # Without mocking, will fail on API call, but tests parameter handling
        assert response.status_code in [401, 500]

    @patch('app.requests.get')
    def test_get_games_api_error(self, mock_get, authenticated_session):
        """Test /api/games handles API errors"""
        from requests.exceptions import RequestException

        mock_get.side_effect = RequestException('API Error')

        response = authenticated_session.get('/api/games/team123')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        assert 'API request failed' in data['error']

    @patch('app.load_demo_data')
    def test_get_games_demo_team_not_found(self, mock_load_demo, authenticated_session):
        """Test /api/games with wrong demo team ID"""
        # Set up demo mode session
        with authenticated_session.session_transaction() as sess:
            sess['demo_mode'] = True

        # Mock demo data with different team ID
        mock_load_demo.return_value = {
            'team': {'id': 'demo_team_123', 'name': 'Demo Team'},
            'games': []
        }

        # Request different team ID
        response = authenticated_session.get('/api/games/wrong_team_id')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        assert 'Demo team not found' in data['error']

    @patch('app.load_demo_data')
    def test_get_games_demo_with_24hour_time(self, mock_load_demo, authenticated_session):
        """Test /api/games demo mode with 24-hour time format"""
        # Set up demo mode session
        with authenticated_session.session_transaction() as sess:
            sess['demo_mode'] = True

        # Mock demo data with 24-hour time format
        mock_load_demo.return_value = {
            'team': {'id': 'demo_team_123', 'name': 'Demo Team'},
            'games': [
                {
                    'id': 'game1',
                    'date': '2024-06-15',
                    'time': '14:30',  # 24-hour format (no AM/PM)
                    'opponent': 'Blue Jays'
                }
            ]
        }

        response = authenticated_session.get('/api/games/demo_team_123')

        assert response.status_code == 200
        data = response.get_json()
        assert 'games' in data
        assert len(data['games']) == 1
        # Should use the time as-is
        assert '14:30' in data['games'][0]['starts_at']


class TestGetAvailabilityRoute:
    """Extended tests for /api/availability route"""

    @patch('app.requests.get')
    def test_get_availability_api_error(self, mock_get, authenticated_session):
        """Test /api/availability handles API errors"""
        from requests.exceptions import RequestException

        mock_get.side_effect = RequestException('Network error')

        response = authenticated_session.get('/api/availability/event123')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data


class TestIndexRoute:
    """Extended tests for index route"""

    def test_index_returns_html(self, client):
        """Test index route returns HTML"""
        response = client.get('/')

        assert response.status_code == 200
        assert response.content_type.startswith('text/html')

    def test_index_with_auth_returns_dashboard(self, authenticated_session):
        """Test authenticated index returns dashboard"""
        response = authenticated_session.get('/')

        assert response.status_code == 200
        # Dashboard should have different content than login
        assert b'html' in response.data.lower()
