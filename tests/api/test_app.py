"""
Basic app tests to verify the Flask application is working correctly
"""

import pytest
import sys
import os

# Add the parent directory to sys.path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_app_exists():
    """Test that the Flask app instance exists"""
    assert app is not None


def test_app_is_in_testing_mode(client):
    """Test that the app is properly configured for testing"""
    assert app.config['TESTING']


def test_dashboard_route(client):
    """Test that the dashboard route exists and returns 200"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Baseball Lineup Manager' in response.data


def test_dashboard_route_content(client):
    """Test that the dashboard contains expected content"""
    response = client.get('/')
    assert response.status_code == 200

    # Check for key elements that should be on the homepage
    content = response.data.decode('utf-8')
    assert 'Baseball Lineup Manager' in content
    assert 'TeamSnap' in content or 'Demo' in content


def test_api_teams_route_exists(client):
    """Test that the teams API route exists (may return 500 without auth)"""
    response = client.get('/api/teams')
    # Without proper auth, this will likely return an error, but route should exist
    assert response.status_code in [200, 401, 500]  # Any of these means route exists


def test_api_games_route_exists(client):
    """Test that the games API route exists"""
    response = client.get('/api/games/test-team-id')
    # Without proper auth/team, this will likely return an error, but route should exist
    assert response.status_code in [200, 400, 401, 500]


def test_api_lineup_route_exists(client):
    """Test that the lineup generation route exists"""
    response = client.post('/api/lineup/generate',
                          json={'team_id': 'test', 'game_id': 'test'})
    # Without proper data, this will return an error, but route should exist
    assert response.status_code in [200, 400, 401, 500]


def test_app_config():
    """Test basic app configuration"""
    assert app.config is not None
    assert hasattr(app, 'route')


def test_flask_version():
    """Test that we're using a compatible Flask version"""
    import flask
    version = flask.__version__
    # Should be using Flask 2.x
    assert version.startswith('2.'), f"Expected Flask 2.x, got {version}"


def test_required_modules_importable():
    """Test that required modules can be imported"""
    try:
        import requests
        import flask
        import os
        import dotenv
        assert True
    except ImportError as e:
        pytest.fail(f"Required module not available: {e}")


def test_environment_loading():
    """Test that environment variables can be loaded"""
    # This should work even if .env doesn't have valid credentials
    from dotenv import load_dotenv
    try:
        load_dotenv()
        # Just test that it doesn't throw an error
        assert True
    except Exception as e:
        pytest.fail(f"Environment loading failed: {e}")