# Testing Examples

This document provides practical examples for common testing patterns in the Baseball Lineup App.

## Table of Contents

1. [Testing Flask Routes](#testing-flask-routes)
2. [Testing Utility Functions](#testing-utility-functions)
3. [Testing Error Handlers](#testing-error-handlers)
4. [Using Test Fixtures](#using-test-fixtures)
5. [Writing Playwright Visual Tests](#writing-playwright-visual-tests)
6. [Mocking External APIs](#mocking-external-apis)
7. [Testing with Different Data](#testing-with-different-data)

---

## Testing Flask Routes

### Example 1: Testing Route with Mocked Session

```python
def test_api_teams_requires_auth(client):
    """Test that /api/teams requires authentication"""
    # Call API without authentication
    response = client.get('/api/teams')

    # Should return 401 Unauthorized
    assert response.status_code == 401
    data = response.get_json()
    assert 'error' in data
    assert 'Not authenticated' in data['error']
```

### Example 2: Testing Route with Authenticated Session

```python
def test_api_teams_with_auth(client):
    """Test /api/teams with authenticated session"""
    # Set up authenticated session
    with client.session_transaction() as sess:
        sess['access_token'] = 'test_token_12345'

    # Call API (will need mocked TeamSnap response)
    response = client.get('/api/teams')

    # Verify response (actual result depends on mocks)
    assert response.status_code in [200, 500]  # 200 if mocked, 500 if real API
```

### Example 3: Testing POST Route with JSON Data

```python
def test_lineup_generation_basic(client):
    """Test lineup generation with valid data"""
    payload = {
        'players': [
            {'id': i, 'name': f'Player {i}', 'position_preferences': []}
            for i in range(1, 10)
        ]
    }

    response = client.post('/api/lineup/generate', json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert 'lineups' in data
    assert len(data['lineups']) > 0
```

### Example 4: Testing Redirects

```python
def test_login_redirects_to_teamsnap(client):
    """Test that login redirects to TeamSnap OAuth"""
    response = client.get('/auth/login', follow_redirects=False)

    assert response.status_code == 302  # Redirect
    assert 'auth.teamsnap.com' in response.location
    assert 'oauth/authorize' in response.location
```

---

## Testing Utility Functions

### Example 5: Testing Pure Function

```python
from app import obfuscate_name

def test_obfuscate_full_name():
    """Test obfuscating a normal full name"""
    result = obfuscate_name("Adam White")
    assert result == "A*** W****"
```

### Example 6: Testing with Edge Cases

```python
def test_obfuscate_name_edge_cases():
    """Test obfuscation with various edge cases"""
    # Empty string
    assert obfuscate_name("") == "Unknown Player"

    # None
    assert obfuscate_name(None) == "Unknown Player"

    # Single letter names
    assert obfuscate_name("A B") == "A B"

    # Unicode characters
    result = obfuscate_name("José García")
    assert result is not None
    assert "*" in result
```

### Example 7: Testing Complex Business Logic

```python
from app import can_fill_all_positions

def test_can_fill_all_positions_success():
    """Test position filling with sufficient players"""
    players = [
        {'id': i, 'position_preferences': []}
        for i in range(1, 10)
    ]
    positions = list(range(1, 10))

    result = can_fill_all_positions(players, positions)
    assert result is True

def test_can_fill_all_positions_impossible():
    """Test position filling with impossible constraints"""
    players = [
        {'id': 1, 'position_preferences': [1]},  # Pitcher only
        {'id': 2, 'position_preferences': [1]},  # Also pitcher only
    ]
    positions = [1, 2]  # Need pitcher AND catcher

    result = can_fill_all_positions(players, positions)
    assert result is False
```

---

## Testing Error Handlers

### Example 8: Testing Error Response Format

```python
def test_error_returns_json(client):
    """Test that errors return proper JSON format"""
    response = client.get('/api/teams')  # No auth

    assert response.status_code == 401
    data = response.get_json()
    assert isinstance(data, dict)
    assert 'error' in data
    assert isinstance(data['error'], str)
```

### Example 9: Testing Exception Handling

```python
from unittest.mock import patch
from requests.exceptions import RequestException

@patch('app.requests.post')
def test_auth_callback_handles_network_error(mock_post, client):
    """Test auth callback handles network failures"""
    # Mock network failure
    mock_post.side_effect = RequestException('Network error')

    response = client.get('/auth/callback?code=test_code')

    assert response.status_code == 400
    assert b'Token exchange failed' in response.data
```

### Example 10: Testing Input Validation

```python
def test_lineup_generation_insufficient_players(client):
    """Test lineup generation with too few players"""
    payload = {'players': [
        {'id': 1, 'name': 'Player 1', 'position_preferences': []},
        {'id': 2, 'name': 'Player 2', 'position_preferences': []},
    ]}

    response = client.post('/api/lineup/generate', json=payload)

    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'at least 9 players' in data['error']
```

---

## Using Test Fixtures

### Example 11: Using Shared Fixtures

```python
# In conftest.py
@pytest.fixture
def authenticated_session(client):
    """Create authenticated session"""
    with client.session_transaction() as sess:
        sess['access_token'] = 'test_token'
    return client

# In test file
def test_with_auth_fixture(authenticated_session):
    """Test using authenticated fixture"""
    response = authenticated_session.get('/api/teams')
    # Session is already set up
    assert response.status_code in [200, 500]
```

### Example 12: Using Custom Data Fixtures

```python
from tests.fixtures.player_data import create_flexible_players

def test_lineup_with_fixture_data(client):
    """Test using player data fixtures"""
    players = create_flexible_players(12)

    payload = {'players': players}
    response = client.post('/api/lineup/generate', json=payload)

    assert response.status_code == 200
    data = response.get_json()
    assert len(data['lineups']) > 0
```

### Example 13: Creating Inline Fixtures

```python
@pytest.fixture
def lineup_payload():
    """Fixture for standard lineup payload"""
    return {
        'players': [
            {'id': i, 'name': f'Player {i}', 'position_preferences': []}
            for i in range(1, 10)
        ]
    }

def test_lineup_with_inline_fixture(client, lineup_payload):
    """Test using inline fixture"""
    response = client.post('/api/lineup/generate', json=lineup_payload)
    assert response.status_code == 200
```

---

## Writing Playwright Visual Tests

### Example 14: Basic Visual Test

```python
from playwright.sync_api import Page, expect

def test_login_page_visual(page: Page, base_url):
    """Test login page visual appearance"""
    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    # Take screenshot and compare
    expect(page).to_have_screenshot("login-page.png")
```

### Example 15: Testing Responsive Layout

```python
def test_dashboard_mobile_layout(page: Page, base_url):
    """Test dashboard on mobile viewport"""
    # Set mobile viewport
    page.set_viewport_size({"width": 375, "height": 667})

    page.goto(f"{base_url}/demo")
    page.wait_for_load_state("networkidle")

    expect(page).to_have_screenshot("dashboard-mobile.png")
```

### Example 16: Testing Interactive State

```python
def test_button_hover_state(page: Page, base_url):
    """Test button hover appearance"""
    page.goto(base_url)

    # Find and hover over button
    button = page.locator("button:has-text('Demo Mode')")
    button.hover()

    # Screenshot with hover state
    expect(page).to_have_screenshot("button-hover.png")
```

---

## Mocking External APIs

### Example 17: Mocking HTTP Request

```python
from unittest.mock import patch, MagicMock

@patch('app.requests.get')
def test_teamsnap_api_failure(mock_get, client):
    """Test handling of TeamSnap API failure"""
    # Set up authenticated session
    with client.session_transaction() as sess:
        sess['access_token'] = 'test_token'

    # Mock API failure
    mock_get.side_effect = Exception('API Error')

    response = client.get('/api/teams')
    assert response.status_code == 500
```

### Example 18: Mocking with Return Value

```python
@patch('app.requests.get')
def test_teamsnap_api_success(mock_get, client):
    """Test successful TeamSnap API call"""
    with client.session_transaction() as sess:
        sess['access_token'] = 'test_token'

    # Mock successful response
    mock_response = MagicMock()
    mock_response.json.return_value = {
        'collection': {
            'items': [{'data': [{'name': 'id', 'value': 'team123'}]}]
        }
    }
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    response = client.get('/api/teams')
    assert response.status_code == 200
```

---

## Testing with Different Data

### Example 19: Parametrized Tests

```python
@pytest.mark.parametrize("player_count,expected_bench", [
    (9, 0),   # No bench with exactly 9 players
    (10, 1),  # 1 on bench
    (12, 3),  # 3 on bench
    (15, 6),  # 6 on bench
])
def test_bench_size(client, player_count, expected_bench):
    """Test bench size with various player counts"""
    payload = {
        'players': [
            {'id': i, 'name': f'Player {i}', 'position_preferences': []}
            for i in range(1, player_count + 1)
        ]
    }

    response = client.post('/api/lineup/generate', json=payload)
    data = response.get_json()

    # Check first lineup bench size
    assert len(data['lineups'][0]['bench']) == expected_bench
```

### Example 20: Testing with Complex Data Scenarios

```python
def test_specialized_positions(client):
    """Test lineup generation with specialized position players"""
    from tests.fixtures.player_data import (
        create_pitchers,
        create_catchers,
        create_infielders,
        create_outfielders
    )

    payload = {
        'players': (
            create_pitchers(2) +
            create_catchers(1, start_id=3) +
            create_infielders(4, start_id=4) +
            create_outfielders(3, start_id=8)
        )
    }

    response = client.post('/api/lineup/generate', json=payload)

    assert response.status_code in [200, 400]
    if response.status_code == 200:
        data = response.get_json()
        # Verify specialized players are assigned appropriately
        assert len(data['lineups']) > 0
```

---

## Summary

These examples cover the most common testing patterns in the Baseball Lineup App:

- ✅ Testing routes with and without authentication
- ✅ Testing utility functions and business logic
- ✅ Testing error handling and edge cases
- ✅ Using fixtures for reusable test data
- ✅ Writing visual regression tests
- ✅ Mocking external dependencies
- ✅ Parametrizing tests for multiple scenarios

For more details, see:
- [Testing Guidelines](guidelines.md)
- [Visual Regression Guide](visual-regression.md)
- [Troubleshooting](troubleshooting.md)
