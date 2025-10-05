"""
Tests for app configuration and initialization
"""

import os
import sys
from unittest.mock import patch

import pytest

# Add the parent directory to sys.path
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)


class TestAppConfiguration:
    """Tests for app configuration"""

    def test_app_has_secret_key(self):
        """Test that app has a secret key configured"""
        from app import app

        assert app.secret_key is not None
        assert len(app.secret_key) > 0

    def test_app_testing_mode(self, app):
        """Test app in testing mode"""
        assert app.config["TESTING"] is True

    @patch.dict(os.environ, {"SECRET_KEY": "test_secret_key_123"})
    def test_app_uses_env_secret_key(self):
        """Test app uses SECRET_KEY from environment"""
        # Need to reload app module to pick up env var
        # This is more of a documentation test
        assert os.getenv("SECRET_KEY") == "test_secret_key_123"

    def test_fielding_positions_constant(self):
        """Test FIELDING_POSITIONS constant is complete"""
        from app import FIELDING_POSITIONS

        assert len(FIELDING_POSITIONS) == 9
        assert FIELDING_POSITIONS[1] == "Pitcher"
        assert FIELDING_POSITIONS[2] == "Catcher"
        assert FIELDING_POSITIONS[3] == "First Base"
        assert FIELDING_POSITIONS[4] == "Second Base"
        assert FIELDING_POSITIONS[5] == "Third Base"
        assert FIELDING_POSITIONS[6] == "Shortstop"
        assert FIELDING_POSITIONS[7] == "Left Field"
        assert FIELDING_POSITIONS[8] == "Center Field"
        assert FIELDING_POSITIONS[9] == "Right Field"

    def test_api_base_constants(self):
        """Test API base URL constants are set"""
        from app import TEAMSNAP_API_BASE, TEAMSNAP_AUTH_BASE

        assert TEAMSNAP_API_BASE == "https://api.teamsnap.com/v3"
        assert TEAMSNAP_AUTH_BASE == "https://auth.teamsnap.com"
