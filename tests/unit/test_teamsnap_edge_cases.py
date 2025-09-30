"""
Tests for TeamSnap API edge cases to reach 98% coverage
Covers date parsing, error handling, and deep API scenarios
"""

import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta, timezone


class TestTeamSnapGamesEdgeCases:
    """Edge cases for /api/games route date parsing and filtering"""

    @patch('app.requests.get')
    def test_game_with_iso_date_no_z_suffix(self, mock_get, authenticated_session):
        """Test game date parsing without 'Z' suffix (line 321)"""
        future_date = (datetime.now(timezone.utc) + timedelta(days=7))
        # Format WITHOUT 'Z' suffix
        date_no_z = future_date.strftime('%Y-%m-%dT%H:%M:%S')

        mock_response = MagicMock()
        mock_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [
                        {'name': 'id', 'value': 'game1'},
                        {'name': 'name', 'value': 'vs Cardinals'},
                        {'name': 'is_game', 'value': True},
                        {'name': 'start_date', 'value': date_no_z}  # No Z!
                    ]
                }]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        response = authenticated_session.get('/api/games/team123')

        assert response.status_code == 200
        data = response.get_json()
        assert 'games' in data
        assert len(data['games']) == 1

    @patch('app.requests.get')
    def test_game_with_include_all_states_true(self, mock_get, authenticated_session):
        """Test include_all_states=true skips date filtering (lines 333-334)"""
        # Past date that would normally be filtered
        past_date = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [
                        {'name': 'id', 'value': 'game1'},
                        {'name': 'name', 'value': 'vs Past Team'},
                        {'name': 'is_game', 'value': True},
                        {'name': 'start_date', 'value': past_date}
                    ]
                }]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        # With include_all_states=true, past games should be included
        response = authenticated_session.get('/api/games/team123?include_all_states=true')

        assert response.status_code == 200
        data = response.get_json()
        assert 'games' in data
        # Past game should be included when include_all_states=true
        assert len(data['games']) == 1

    @patch('app.requests.get')
    def test_game_too_far_in_future(self, mock_get, authenticated_session):
        """Test game rejection for dates >30 days in future (lines 355-357)"""
        # 60 days in future
        far_future = (datetime.now(timezone.utc) + timedelta(days=60)).isoformat()

        mock_response = MagicMock()
        mock_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [
                        {'name': 'id', 'value': 'game1'},
                        {'name': 'name', 'value': 'vs Future Team'},
                        {'name': 'is_game', 'value': True},
                        {'name': 'start_date', 'value': far_future}
                    ]
                }]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        response = authenticated_session.get('/api/games/team123')

        assert response.status_code == 200
        data = response.get_json()
        assert 'games' in data
        # Too far in future, should be filtered out
        assert len(data['games']) == 0

    @patch('app.requests.get')
    def test_game_with_invalid_date_format(self, mock_get, authenticated_session):
        """Test date parsing error handling (lines 359-361)"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [
                        {'name': 'id', 'value': 'game1'},
                        {'name': 'name', 'value': 'vs Bad Date Team'},
                        {'name': 'is_game', 'value': True},
                        {'name': 'start_date', 'value': 'not-a-valid-date'}  # Invalid!
                    ]
                }]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        response = authenticated_session.get('/api/games/team456')

        assert response.status_code == 200
        data = response.get_json()
        assert 'games' in data
        # Invalid date should be skipped (continue in except block)
        assert len(data['games']) == 0

    @patch('app.requests.get')
    def test_game_missing_start_date(self, mock_get, authenticated_session):
        """Test game without start_date field (line 366)"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [
                        {'name': 'id', 'value': 'game1'},
                        {'name': 'name', 'value': 'vs No Date Team'},
                        {'name': 'is_game', 'value': True}
                        # No start_date field!
                    ]
                }]
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response

        response = authenticated_session.get('/api/games/team789')

        assert response.status_code == 200
        data = response.get_json()
        assert 'games' in data
        # No start date, should be skipped
        assert len(data['games']) == 0


class TestTeamSnapAvailabilityEdgeCases:
    """Edge cases for /api/availability route"""

    @patch('app.requests.get')
    def test_availability_member_fetch_failure(self, mock_get, authenticated_session):
        """Test availability when member fetch fails (lines 483-487)"""
        # Mock availability response
        mock_avail_response = MagicMock()
        mock_avail_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [
                        {'name': 'member_id', 'value': 'member1'},
                        {'name': 'status_code', 'value': 1}  # Available
                    ]
                }]
            }
        }
        mock_avail_response.raise_for_status = MagicMock()

        # Mock member details with non-200 status
        mock_member_response = MagicMock()
        mock_member_response.status_code = 404  # Failed!
        mock_member_response.raise_for_status = MagicMock()

        # Return different responses for availability and member calls
        mock_get.side_effect = [mock_avail_response, mock_member_response]

        response = authenticated_session.get('/api/availability/event999')

        assert response.status_code == 200
        data = response.get_json()
        assert 'attending_players' in data
        # Member fetch failed, should be skipped
        assert len(data['attending_players']) == 0

    @patch('app.requests.get')
    def test_availability_non_player_member(self, mock_get, authenticated_session):
        """Test availability filters out non-players (coaches/managers) (line 483)"""
        # Mock availability response
        mock_avail_response = MagicMock()
        mock_avail_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [
                        {'name': 'member_id', 'value': 'member_coach'},
                        {'name': 'status_code', 'value': 1}
                    ]
                }]
            }
        }
        mock_avail_response.raise_for_status = MagicMock()

        # Mock member details - is_manager=True (coach/manager)
        mock_member_response = MagicMock()
        mock_member_response.status_code = 200
        mock_member_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [
                        {'name': 'id', 'value': 'member_coach'},
                        {'name': 'first_name', 'value': 'Coach'},
                        {'name': 'last_name', 'value': 'Smith'},
                        {'name': 'type', 'value': 'coach'},
                        {'name': 'is_manager', 'value': True}  # Manager!
                    ]
                }]
            }
        }
        mock_member_response.raise_for_status = MagicMock()

        mock_get.side_effect = [mock_avail_response, mock_member_response]

        response = authenticated_session.get('/api/availability/event_coach')

        assert response.status_code == 200
        data = response.get_json()
        assert 'attending_players' in data
        # Manager should be filtered out
        assert len(data['attending_players']) == 0


    @patch('app.requests.get')
    def test_availability_member_not_attending(self, mock_get, authenticated_session):
        """Test availability skips non-attending members (line 487)"""
        # Mock availability response with status_code != 1 (not attending)
        mock_avail_response = MagicMock()
        mock_avail_response.json.return_value = {
            'collection': {
                'items': [{
                    'data': [
                        {'name': 'member_id', 'value': 'member_absent'},
                        {'name': 'status_code', 'value': 0}  # Not attending!
                    ]
                }]
            }
        }
        mock_avail_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_avail_response

        response = authenticated_session.get('/api/availability/event_skip')

        assert response.status_code == 200
        data = response.get_json()
        assert 'attending_players' in data
        # Not attending, should be skipped
        assert len(data['attending_players']) == 0


class TestAvailabilityDemoMode:
    """Test demo mode edge cases for availability endpoint"""

    @patch('app.load_demo_data')
    def test_availability_demo_game_not_found(self, mock_load_demo, authenticated_session):
        """Test availability with wrong demo game ID (line 399)"""
        # Set up demo mode session
        with authenticated_session.session_transaction() as sess:
            sess['demo_mode'] = True

        # Mock demo data with different game ID
        mock_load_demo.return_value = {
            'team': {'id': 'demo_team_123'},
            'games': [{'id': 'demo_game_456'}]
        }

        # Request different game ID
        response = authenticated_session.get('/api/availability/wrong_game_id')

        assert response.status_code == 404
        data = response.get_json()
        assert 'error' in data
        # TODO(#34): Replace with error code assertion once implemented
        # assert data['code'] == 'DEMO_GAME_NOT_FOUND'
        assert 'Demo game not found' in data['error']

    @patch('app.load_demo_data')
    def test_availability_demo_data_unavailable(self, mock_load_demo, authenticated_session):
        """Test availability when demo data fails to load (lines 400-401)"""
        # Set up demo mode session
        with authenticated_session.session_transaction() as sess:
            sess['demo_mode'] = True

        # Mock load_demo_data returns None (failure)
        mock_load_demo.return_value = None

        response = authenticated_session.get('/api/availability/any_game')

        assert response.status_code == 500
        data = response.get_json()
        assert 'error' in data
        # TODO(#34): Replace with error code assertion once implemented
        # assert data['code'] == 'DEMO_DATA_UNAVAILABLE'
        assert 'Demo data not available' in data['error']


class TestObfuscationErrorHandling:
    """Test error handling in obfuscate_name function"""

    def test_obfuscate_name_with_none(self):
        """Test obfuscate_name handles None gracefully"""
        from app import obfuscate_name

        # None input should return "Unknown Player"
        result = obfuscate_name(None)
        assert result == "Unknown Player"

    def test_obfuscate_name_with_empty_string(self):
        """Test obfuscate_name handles empty string"""
        from app import obfuscate_name

        # Empty string should return "Unknown Player"
        result = obfuscate_name("")
        assert result == "Unknown Player"

    def test_obfuscate_name_with_whitespace_only(self):
        """Test obfuscate_name handles whitespace-only string"""
        from app import obfuscate_name

        # Whitespace should return "Unknown Player"
        result = obfuscate_name("   ")
        assert result == "Unknown Player"
