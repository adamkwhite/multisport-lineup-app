# Testing Guidelines

## Testing Philosophy

We believe in comprehensive, maintainable tests that give us confidence to refactor and ship quickly. Our testing strategy balances coverage goals with practical development velocity.

### Core Principles

1. **Test Behavior, Not Implementation** - Tests should verify what the code does, not how it does it
2. **Fast Feedback** - Unit tests should run in under 10 seconds
3. **Readable Tests** - Tests are documentation; they should be self-explanatory
4. **Fail Fast** - Tests should fail immediately when something breaks
5. **No Flaky Tests** - Tests must be deterministic and reliable

### Coverage Goals

- **Overall target**: 90% for app.py
- **Utility functions**: 100% (simple, critical functions)
- **Business logic**: 95% (lineup generation, position assignment)
- **Route handlers**: 85% (exclude production-only code)
- **Error handlers**: 95% (critical for reliability)

## When to Write Each Type of Test

### Unit Tests (`tests/unit/`)

**When to use:**
- Testing individual functions in isolation
- Testing Flask routes with mocked dependencies
- Testing utility functions (obfuscation, validation)
- Testing business logic (lineup generation)

**Characteristics:**
- Fast (< 10 seconds total)
- No external dependencies
- Use mocks/fixtures
- Test one thing at a time

**Example:**
```python
def test_obfuscate_name():
    """Test basic name obfuscation"""
    assert obfuscate_name("John Smith") == "J*** S****"
```

### Edge Case Tests (`tests/edge_cases/`)

**When to use:**
- Testing boundary conditions
- Testing error handling
- Testing unusual inputs
- Testing constraint conflicts

**Characteristics:**
- Focus on "what if" scenarios
- Test with extreme values
- Test with invalid inputs
- Document expected failure modes

**Example:**
```python
def test_lineup_with_impossible_constraints():
    """Test when all players want same position"""
    # Should handle gracefully with fallback
```

### Visual Regression Tests (`tests/visual/`)

**When to use:**
- Testing UI components
- Testing responsive layouts
- Testing print styles
- Catching unintended visual changes

**Characteristics:**
- Require running application
- Use Playwright for screenshots
- Compare with baseline images
- Test multiple viewports

**Example:**
```python
def test_dashboard_layout(page: Page):
    """Test dashboard visual layout"""
    expect(page).to_have_screenshot("dashboard.png")
```

## Test Organization

### File Naming Conventions

```
tests/
├── unit/
│   ├── test_auth_routes.py      # Tests for auth-related routes
│   ├── test_lineup_generation.py # Tests for lineup logic
│   └── test_utility_functions.py # Tests for utilities
├── edge_cases/
│   ├── test_edge_case_lineup.py  # Edge cases for lineup
│   ├── test_edge_case_obfuscation.py
│   └── test_edge_case_errors.py  # Error handling tests
├── visual/
│   ├── test_visual_login.py      # Visual tests for login
│   ├── test_visual_dashboard.py  # Visual tests for dashboard
│   └── test_visual_lineup.py     # Visual tests for lineup
└── fixtures/
    ├── player_data.py            # Reusable player fixtures
    ├── game_data.py              # Reusable game fixtures
    └── session_helpers.py        # Session management helpers
```

### Test Class Organization

Group related tests in classes:

```python
class TestObfuscateName:
    """Tests for obfuscate_name function"""

    def test_full_name(self):
        """Test with standard full name"""
        pass

    def test_single_name(self):
        """Test with single name only"""
        pass
```

### Test Naming

Follow the pattern: `test_<what>_<condition>`

**Good:**
- `test_lineup_generation_with_9_players`
- `test_obfuscate_name_with_unicode`
- `test_login_redirects_to_teamsnap`

**Bad:**
- `test_1`, `test_case_2`
- `test_function`, `test_works`
- `test_bug_fix` (what bug?)

## Using Fixtures

### Shared Fixtures (`conftest.py`)

```python
@pytest.fixture
def client(app):
    """Create Flask test client"""
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def authenticated_session(client):
    """Client with authenticated session"""
    with client.session_transaction() as sess:
        sess['access_token'] = 'test_token'
    return client
```

### Custom Fixtures (`tests/fixtures/`)

Reusable test data should be in fixture modules:

```python
from tests.fixtures.player_data import create_flexible_players

def test_lineup_generation():
    players = create_flexible_players(9)
    # Use in test...
```

### Fixture Scope

- `function` (default) - New fixture per test
- `class` - Shared across test class
- `module` - Shared across test file
- `session` - Shared across all tests

Use broader scope for expensive setup (Playwright browsers).

## Avoiding Test Duplication

### Use Parametrize for Similar Tests

Instead of:
```python
def test_9_players():
    assert generate_lineup(9) is not None

def test_10_players():
    assert generate_lineup(10) is not None
```

Do:
```python
@pytest.mark.parametrize("count", [9, 10, 12, 15])
def test_lineup_with_various_counts(count):
    assert generate_lineup(count) is not None
```

### Use Helper Functions

```python
def assert_valid_lineup(lineup):
    """Reusable assertion for lineup validation"""
    assert len(lineup['lineup']) == 9
    assert all(pos in lineup['lineup'] for pos in range(1, 10))

def test_lineup_basic():
    lineup = generate_lineup()
    assert_valid_lineup(lineup)
```

## Test Independence

Each test should:
- Set up its own data
- Clean up after itself
- Not depend on other tests
- Work in any order

**Bad (tests depend on each other):**
```python
user = None

def test_create_user():
    global user
    user = create_user()

def test_user_name():
    assert user.name == "Test"  # Fails if test_create_user didn't run
```

**Good (tests are independent):**
```python
def test_create_user():
    user = create_user()
    assert user is not None

def test_user_name():
    user = create_user()
    assert user.name == "Test"
```

## Mocking External Dependencies

Use `pytest-mock` or `unittest.mock` for external APIs:

```python
def test_api_call_handles_failure(client, mocker):
    """Test API failure handling"""
    mock_requests = mocker.patch('app.requests.get')
    mock_requests.side_effect = RequestException('Network error')

    response = client.get('/api/teams')
    assert response.status_code == 500
```

## Assertions

### Use Specific Assertions

**Good:**
```python
assert result == expected
assert 'error' in response.json()
assert len(lineup) == 9
```

**Bad:**
```python
assert result  # Too vague
assert response  # What are we checking?
```

### Test Error Messages

```python
def test_insufficient_players_error_message():
    response = client.post('/api/lineup/generate', json={'players': []})
    assert response.status_code == 400
    assert 'at least 9 players' in response.json()['error']
```

## Running Tests

### Run all tests:
```bash
./lineup-venv/bin/pytest
```

### Run specific test file:
```bash
./lineup-venv/bin/pytest tests/unit/test_lineup_generation.py
```

### Run specific test:
```bash
./lineup-venv/bin/pytest tests/unit/test_lineup_generation.py::test_exactly_9_players
```

### Run with coverage:
```bash
./lineup-venv/bin/pytest --cov=app --cov-report=term-missing
```

### Run only fast tests (skip visual):
```bash
./lineup-venv/bin/pytest tests/unit/ tests/edge_cases/
```

## Best Practices Summary

1. ✅ Write tests first (TDD) or alongside code
2. ✅ Keep tests simple and focused
3. ✅ Use descriptive test names
4. ✅ Test edge cases and error conditions
5. ✅ Use fixtures to reduce duplication
6. ✅ Make tests independent and isolated
7. ✅ Mock external dependencies
8. ✅ Keep test execution time under 10s (unit tests)
9. ✅ Aim for 90% coverage on critical code
10. ✅ Review test failures before modifying tests

## What NOT to Test

- Framework code (Flask, pytest internals)
- Third-party libraries (TeamSnap API internals)
- Trivial getters/setters
- Generated code
- Deprecated code scheduled for removal

Focus testing effort on:
- Business logic
- User-facing features
- Error handling
- Edge cases
- Security-critical code
