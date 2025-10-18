"""
Shared pytest fixtures and configuration for all tests
"""

import os
import sys

import pytest

# Add the parent directory to sys.path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app


@pytest.fixture
def app():
    """Create Flask app instance for testing"""
    flask_app.config["TESTING"] = True
    flask_app.config["SECRET_KEY"] = "test-secret-key"
    flask_app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for tests
    return flask_app


@pytest.fixture
def client(app):
    """Create a test client for the Flask application"""
    with app.test_client() as client:
        with app.app_context():
            yield client


@pytest.fixture
def authenticated_session(client):
    """Create a session with mock authentication"""
    with client.session_transaction() as sess:
        sess["access_token"] = "test_token_12345"
    return client


@pytest.fixture
def demo_session(client):
    """Create a session with demo mode enabled"""
    with client.session_transaction() as sess:
        sess["demo_mode"] = True
        sess["access_token"] = "demo_token"
    return client


# Playwright fixtures are automatically provided by pytest-playwright
# Additional Playwright configuration can be added here if needed
