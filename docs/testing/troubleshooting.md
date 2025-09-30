# Testing Troubleshooting Guide

Common test failures and solutions for the Baseball Lineup App.

## Table of Contents

1. [Test Execution Issues](#test-execution-issues)
2. [Assertion Failures](#assertion-failures)
3. [Mock/Fixture Issues](#mockfixture-issues)
4. [Visual Test Issues](#visual-test-issues)
5. [Coverage Issues](#coverage-issues)
6. [Performance Issues](#performance-issues)

---

## Test Execution Issues

### Problem: `ModuleNotFoundError: No module named 'app'`

**Cause**: Python path not set correctly.

**Solution**:
```python
# Add at top of test file
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import function_name
```

Or run tests from project root:
```bash
cd /home/adam/Code/baseball-lineup-app
./baseball-venv/bin/pytest tests/
```

### Problem: `ImportError: cannot import name 'function_name'`

**Cause**: Function doesn't exist or isn't exported.

**Solution**:
1. Verify function exists in app.py
2. Check spelling/capitalization
3. Ensure function is at module level (not nested)

### Problem: Tests run but skip everything

**Cause**: Tests marked with `@pytest.mark.skip`.

**Solution**:
```bash
# Run including skipped tests
./baseball-venv/bin/pytest -v -m "not skip"

# Or remove skip decorator from test file
```

### Problem: `fixture 'client' not found`

**Cause**: Fixture not defined in conftest.py or wrong scope.

**Solution**:
1. Check tests/conftest.py has the fixture
2. Verify fixture name matches
3. Ensure conftest.py is in correct directory

---

## Assertion Failures

### Problem: `AssertionError: assert 500 == 200`

**Cause**: Route returned error instead of success.

**Debug Steps**:
```python
def test_debug_response(client):
    response = client.get('/api/endpoint')

    # Print response for debugging
    print(f"Status: {response.status_code}")
    print(f"Data: {response.get_json()}")
    print(f"Headers: {response.headers}")

    assert response.status_code == 200
```

**Common Causes**:
- Missing authentication
- Invalid input data
- Database/API not available
- Unhandled exception in route

### Problem: `AssertionError: assert 'key' in {}`

**Cause**: Expected key not in response.

**Debug**:
```python
data = response.get_json()
print(f"Available keys: {data.keys() if data else 'None'}")
print(f"Full response: {data}")

assert 'expected_key' in data
```

### Problem: `AssertionError: assert None is not None`

**Cause**: Function returned None unexpectedly.

**Debug**:
```python
result = some_function()
print(f"Result type: {type(result)}")
print(f"Result value: {result}")

assert result is not None
```

---

## Mock/Fixture Issues

### Problem: Mock not being called

**Cause**: Mocking wrong function or wrong import path.

**Debug**:
```python
from unittest.mock import patch

@patch('app.requests.get')  # Patch where it's used, not where it's defined
def test_api_call(mock_get):
    mock_get.return_value = MagicMock()

    # ... test code ...

    # Verify mock was called
    assert mock_get.called
    print(f"Call count: {mock_get.call_count}")
    print(f"Call args: {mock_get.call_args}")
```

### Problem: Fixture not updating session

**Cause**: Session transaction context not used correctly.

**Solution**:
```python
# Correct way
def test_with_session(client):
    with client.session_transaction() as sess:
        sess['key'] = 'value'
    # Session is saved here

    response = client.get('/route')
    # Session is available

# Wrong way
def test_with_session(client):
    client.session['key'] = 'value'  # Doesn't work with Flask test client
```

### Problem: Mock side_effect not working

**Cause**: side_effect expects iterable or callable.

**Solution**:
```python
# For exception
mock.side_effect = Exception('Error')

# For sequence of return values
mock.side_effect = [value1, value2, value3]

# For callable
def side_effect_function(*args, **kwargs):
    return calculated_value
mock.side_effect = side_effect_function
```

---

## Visual Test Issues

### Problem: `Executable doesn't exist at /path/to/chromium`

**Cause**: Playwright browsers not installed.

**Solution**:
```bash
./baseball-venv/bin/playwright install chromium
```

### Problem: Screenshots always differ

**Cause**: Dynamic content (timestamps, animations, random data).

**Solution**:
```python
def test_stable_screenshot(page: Page, base_url):
    page.goto(base_url)

    # Hide dynamic content
    page.evaluate("""
        document.querySelectorAll('.timestamp').forEach(el => el.style.display = 'none');
        document.querySelectorAll('[data-random]').forEach(el => el.textContent = 'MOCK');
    """)

    # Wait for animations
    page.wait_for_timeout(500)

    expect(page).to_have_screenshot("stable.png")
```

### Problem: Visual tests timeout

**Cause**: Page not loading, network issue, or slow page.

**Solution**:
```python
# Increase timeout
page.set_default_timeout(30000)  # 30 seconds

# Wait more specifically
page.wait_for_selector(".content", state="visible")

# Check page loaded
page.wait_for_load_state("networkidle")
```

### Problem: Can't find element

**Cause**: Selector doesn't match or element not loaded.

**Debug**:
```python
# Print page content
print(page.content())

# Take debug screenshot
page.screenshot(path="debug.png")

# Try more flexible selector
page.locator("text=Login")  # By text
page.locator("button").filter(has_text="Login")  # By role and text
```

---

## Coverage Issues

### Problem: Coverage shows 0%

**Cause**: Source file not found or wrong path.

**Solution**:
```bash
# Run from project root
cd /home/adam/Code/baseball-lineup-app
./baseball-venv/bin/pytest --cov=app --cov-report=term-missing

# Check coverage config in pytest.ini
[tool:pytest]
addopts = --cov=app --cov-report=term-missing
```

### Problem: Coverage doesn't match expected

**Cause**: Not all test files run.

**Solution**:
```bash
# Run all test directories
./baseball-venv/bin/pytest tests/unit/ tests/edge_cases/ --cov=app

# Verify all tests collected
./baseball-venv/bin/pytest --collect-only | grep collected
```

### Problem: Specific lines show as uncovered

**Cause**: Code path not tested.

**Debug**:
```bash
# See which lines are missing
./baseball-venv/bin/pytest --cov=app --cov-report=term-missing

# Focus on specific file
./baseball-venv/bin/pytest --cov=app --cov-report=annotate
# Check app.py,cover file
```

**Solution**: Add tests for missing code paths (error handlers, edge cases).

---

## Performance Issues

### Problem: Tests take too long

**Cause**: Too many tests, slow fixtures, or unnecessary waits.

**Profile Tests**:
```bash
# Show slowest tests
./baseball-venv/bin/pytest --durations=10

# Show all test durations
./baseball-venv/bin/pytest --durations=0
```

**Solutions**:
1. Use session-scoped fixtures for expensive setup
2. Mock external API calls
3. Remove unnecessary `sleep()` or `wait_for_timeout()`
4. Run unit tests separately from visual tests

### Problem: Specific test is slow

**Debug**:
```python
import time

def test_slow_function():
    start = time.time()

    # Test code
    result = slow_function()

    duration = time.time() - start
    print(f"Test took {duration:.2f} seconds")

    assert result is not None
```

**Solutions**:
- Mock slow external calls
- Use smaller test datasets
- Optimize the function being tested

### Problem: Visual tests are slow

**Cause**: Browser startup, page loads, network waits.

**Solutions**:
```python
# Use session-scoped browser
@pytest.fixture(scope="session")
def browser():
    browser = playwright.chromium.launch()
    yield browser
    browser.close()

# Skip visual tests in unit test runs
pytest tests/unit/ tests/edge_cases/  # Fast
pytest tests/visual/  # Slow, run separately
```

---

## Common Patterns

### Debugging Failed Tests

1. **Add print statements**:
   ```python
   print(f"Value: {value}")
   print(f"Type: {type(value)}")
   ```

2. **Use pytest -vv for verbose output**:
   ```bash
   ./baseball-venv/bin/pytest tests/test_file.py::test_name -vv
   ```

3. **Use pytest -s to see print output**:
   ```bash
   ./baseball-venv/bin/pytest tests/test_file.py -s
   ```

4. **Run single test**:
   ```bash
   ./baseball-venv/bin/pytest tests/test_file.py::TestClass::test_method -v
   ```

5. **Use pytest --pdb to debug**:
   ```bash
   ./baseball-venv/bin/pytest tests/test_file.py --pdb
   ```

### Fixing Flaky Tests

**Flaky tests** pass/fail inconsistently.

**Common Causes**:
1. Race conditions
2. Timing dependencies
3. External dependencies
4. Shared state between tests

**Solutions**:
1. Add explicit waits
2. Use mocks for external services
3. Ensure test independence
4. Use fixtures for clean state

### Test Cleanup

```python
@pytest.fixture
def resource():
    # Setup
    r = create_resource()

    yield r

    # Cleanup (runs after test)
    r.cleanup()
```

---

## Getting Help

### Check Test Output

```bash
# Run with full traceback
./baseball-venv/bin/pytest tests/ --tb=long

# Run with short traceback
./baseball-venv/bin/pytest tests/ --tb=short

# Run with no traceback (just failures)
./baseball-venv/bin/pytest tests/ --tb=line
```

### Pytest Options

```bash
# Show all available options
./baseball-venv/bin/pytest --help

# Show fixture details
./baseball-venv/bin/pytest --fixtures

# Show available markers
./baseball-venv/bin/pytest --markers
```

### Common Commands

```bash
# Run specific test file
pytest tests/unit/test_auth_routes.py

# Run tests matching pattern
pytest -k "test_login"

# Run tests with marker
pytest -m "slow"

# Stop after first failure
pytest -x

# Show local variables in traceback
pytest -l

# Collect tests without running
pytest --collect-only
```

---

## Summary

Most test issues fall into these categories:

1. **Setup Problems**: Missing imports, wrong paths, fixtures not found
2. **Logic Errors**: Incorrect assertions, wrong expected values
3. **Environment Issues**: Missing dependencies, wrong Python version
4. **Timing Issues**: Races, timeouts, flaky tests
5. **Mock Issues**: Wrong patch path, side_effect problems

**General Debugging Approach**:
1. Read the error message carefully
2. Add print statements to understand state
3. Run single failing test in isolation
4. Check if issue is test-specific or general
5. Verify assumptions with simple assertions
6. Use pytest debugging options (-vv, -s, --pdb)

For more help, see:
- [Testing Guidelines](guidelines.md)
- [Testing Examples](examples.md)
- [Visual Regression Guide](visual-regression.md)
