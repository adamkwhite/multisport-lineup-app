# Visual Regression Testing Guide

Visual regression testing uses Playwright to capture screenshots and detect unintended UI changes.

## Table of Contents

1. [Setup](#setup)
2. [Running Tests](#running-tests)
3. [Writing Visual Tests](#writing-visual-tests)
4. [Managing Baselines](#managing-baselines)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

---

## Setup

### 1. Install Playwright

Playwright should already be installed. Verify:

```bash
./lineup-venv/bin/pip list | grep playwright
```

Should show:
```
playwright               1.55.0
pytest-playwright        0.7.1
```

### 2. Install Browser Binaries

```bash
./lineup-venv/bin/playwright install chromium
```

This downloads the Chromium browser (~174MB).

### 3. Start the Application

Visual tests require the Flask app to be running:

```bash
./start.sh
```

Or manually:

```bash
./lineup-venv/bin/python app.py
```

Verify app is running at `http://localhost:5001`

---

## Running Tests

### Run All Visual Tests

```bash
./lineup-venv/bin/pytest tests/visual/ -v
```

Note: Tests are marked with `@pytest.mark.skip` by default. To run:

```bash
./lineup-venv/bin/pytest tests/visual/ -v -m "not skip"
```

Or remove the skip decorator from test files.

### Run Specific Test File

```bash
./lineup-venv/bin/pytest tests/visual/test_visual_login.py -v
```

### Run in Headed Mode (See Browser)

```bash
./lineup-venv/bin/pytest tests/visual/ -v --headed
```

Add `--slowmo=1000` to slow down actions:

```bash
./lineup-venv/bin/pytest tests/visual/ -v --headed --slowmo=1000
```

### Run Specific Test

```bash
./lineup-venv/bin/pytest tests/visual/test_visual_login.py::TestLoginPageVisuals::test_login_page_initial_state -v
```

---

## Writing Visual Tests

### Basic Visual Test Structure

```python
import pytest
from playwright.sync_api import Page, expect


@pytest.mark.skip(reason="Requires app to be running")
class TestMyPageVisuals:
    """Visual tests for my page"""

    def test_page_appearance(self, page: Page, base_url):
        """Test page visual appearance"""
        # Navigate to page
        page.goto(f"{base_url}/my-page")

        # Wait for content to load
        page.wait_for_load_state("networkidle")

        # Take screenshot and compare
        expect(page).to_have_screenshot("my-page.png")
```

### Using Fixtures

#### Base URL Fixture

```python
def test_with_base_url(page: Page, base_url):
    """Use base_url fixture"""
    page.goto(base_url)  # Goes to http://localhost:5001
```

#### Authenticated Page Fixture

```python
def test_authenticated_view(authenticated_page: Page):
    """Use authenticated_page fixture"""
    # Page is already authenticated via demo mode
    authenticated_page.wait_for_load_state("networkidle")
    expect(authenticated_page).to_have_screenshot("auth-view.png")
```

### Waiting for Content

Always wait for content to load before taking screenshots:

```python
# Wait for network to be idle
page.wait_for_load_state("networkidle")

# Wait for specific element
page.wait_for_selector("[data-testid='team-list']")

# Wait for timeout (use sparingly)
page.wait_for_timeout(1000)  # 1 second

# Wait for navigation
page.wait_for_url("http://localhost:5001/dashboard")
```

### Testing Responsive Layouts

```python
def test_mobile_layout(page: Page, base_url):
    """Test mobile viewport"""
    # Set mobile viewport
    page.set_viewport_size({"width": 375, "height": 667})

    page.goto(base_url)
    page.wait_for_load_state("networkidle")

    expect(page).to_have_screenshot("mobile-view.png")

def test_tablet_layout(page: Page, base_url):
    """Test tablet viewport"""
    page.set_viewport_size({"width": 768, "height": 1024})
    page.goto(base_url)
    page.wait_for_load_state("networkidle")
    expect(page).to_have_screenshot("tablet-view.png")
```

### Testing Print Styles

```python
def test_print_layout(page: Page, base_url):
    """Test print-friendly view"""
    page.goto(f"{base_url}/lineup")
    page.wait_for_load_state("networkidle")

    # Emulate print media
    page.emulate_media(media="print")

    expect(page).to_have_screenshot("print-view.png")
```

### Testing Interactive States

```python
def test_button_hover(page: Page, base_url):
    """Test button hover state"""
    page.goto(base_url)

    # Hover over element
    button = page.locator("button:has-text('Login')")
    button.hover()

    expect(page).to_have_screenshot("button-hover.png")

def test_form_focused(page: Page, base_url):
    """Test input focus state"""
    page.goto(f"{base_url}/form")

    # Focus input
    input_field = page.locator("input[name='username']")
    input_field.focus()

    expect(page).to_have_screenshot("input-focused.png")
```

---

## Managing Baselines

### First Run: Generate Baselines

On first run, Playwright generates baseline screenshots:

```bash
./lineup-venv/bin/pytest tests/visual/ -v
```

Baselines are stored in:
```
tests/visual/
├── test_visual_login.py-snapshots/
│   ├── login-page-initial.png
│   ├── login-page-mobile.png
│   └── ...
├── test_visual_dashboard.py-snapshots/
└── test_visual_lineup.py-snapshots/
```

### Reviewing Baselines

After first run:

1. Check generated screenshots
2. Verify they look correct
3. Commit baselines to git:

```bash
git add tests/visual/*-snapshots/
git commit -m "Add visual regression test baselines"
```

### Updating Baselines

When UI changes are intentional, update baselines:

```bash
./lineup-venv/bin/pytest tests/visual/ --update-snapshots
```

This regenerates all baseline screenshots.

### Updating Specific Test Baselines

```bash
./lineup-venv/bin/pytest tests/visual/test_visual_login.py --update-snapshots
```

### Viewing Diff Reports

When tests fail, Playwright generates diff reports:

```bash
playwright-report/
├── index.html          # Open in browser
└── data/
    ├── actual.png      # Current screenshot
    ├── expected.png    # Baseline
    └── diff.png        # Highlighted differences
```

View the report:

```bash
./lineup-venv/bin/playwright show-report
```

---

## Best Practices

### 1. Use Stable Selectors

Prefer `data-testid` attributes:

```html
<button data-testid="submit-button">Submit</button>
```

```python
page.locator("[data-testid='submit-button']").click()
```

### 2. Wait for Dynamic Content

```python
# Wait for API calls to complete
page.wait_for_load_state("networkidle")

# Wait for animations to finish
page.wait_for_timeout(500)

# Wait for specific element
page.wait_for_selector(".loaded")
```

### 3. Hide Dynamic Content

Mock timestamps, random data, or hide dynamic elements:

```python
# Hide dynamic timestamp
page.evaluate("document.querySelector('.timestamp').style.display = 'none'")

# Mock date
page.evaluate("Date.now = () => 1640000000000")
```

### 4. Use Consistent Viewport

Default viewport is 1280x720. Stick to it or document changes:

```python
# Good - uses default
page.goto(base_url)

# Good - documents mobile test
def test_mobile_layout(page: Page):
    page.set_viewport_size({"width": 375, "height": 667})
```

### 5. Name Screenshots Descriptively

```python
# Good
expect(page).to_have_screenshot("login-page-initial-state.png")
expect(page).to_have_screenshot("dashboard-with-teams-loaded.png")

# Bad
expect(page).to_have_screenshot("test1.png")
expect(page).to_have_screenshot("screenshot.png")
```

### 6. Test Critical User Paths

Focus visual tests on:
- Main user flows (login, lineup generation)
- Complex layouts (baseball diamond graphic)
- Responsive breakpoints
- Print styles
- Error states

Don't test:
- Every minor UI variation
- Trivial color changes
- Internal admin pages

### 7. Keep Tests Independent

Each test should:
- Set up its own state
- Navigate to its own page
- Not depend on other tests

---

## Troubleshooting

### Tests Fail: "Application not running"

**Problem**: Flask app is not running.

**Solution**:
```bash
./start.sh
```

Verify at `http://localhost:5001`

### Tests Fail: Screenshots Differ

**Problem**: Genuine UI change or environment difference.

**Solution**:
1. View diff report: `./lineup-venv/bin/playwright show-report`
2. If change is intentional: `pytest tests/visual/ --update-snapshots`
3. If not intentional: Fix the UI bug

### Tests Are Flaky

**Problem**: Tests pass/fail inconsistently.

**Solution**:
- Add explicit waits: `page.wait_for_load_state("networkidle")`
- Hide dynamic content (timestamps, animations)
- Increase timeout: `page.set_default_timeout(30000)`
- Use stable selectors (data-testid)

### Screenshots Look Different on CI

**Problem**: Different environment (fonts, browser version).

**Solution**:
- Use Docker for consistent environment
- Pin browser version: `playwright install chromium@1.40.0`
- Commit baselines generated in CI environment

### Tests Timeout

**Problem**: Page takes too long to load.

**Solution**:
```python
# Increase timeout
page.set_default_timeout(30000)  # 30 seconds

# Wait for specific condition
page.wait_for_selector(".content", timeout=10000)
```

### Can't Find Element

**Problem**: Selector doesn't match any elements.

**Solution**:
```python
# Debug: Print page content
print(page.content())

# Debug: Take screenshot
page.screenshot(path="debug.png")

# Use more flexible selector
page.locator("button").filter(has_text="Login")
```

---

## CI/CD Integration

### Running in CI

```yaml
# .github/workflows/visual-tests.yml
- name: Install Playwright browsers
  run: playwright install chromium

- name: Start Flask app
  run: |
    python app.py &
    sleep 5  # Wait for app to start

- name: Run visual tests
  run: pytest tests/visual/ --headed=false

- name: Upload test report
  if: failure()
  uses: actions/upload-artifact@v3
  with:
    name: playwright-report
    path: playwright-report/
```

### Baseline Management in CI

1. Generate baselines locally
2. Commit to git
3. CI compares against committed baselines
4. On failure, upload diff report as artifact

---

## Summary

Visual regression testing with Playwright helps catch unintended UI changes:

- ✅ Install Playwright and browsers
- ✅ Start Flask app before running tests
- ✅ Write tests with `expect(page).to_have_screenshot()`
- ✅ Generate and commit baseline screenshots
- ✅ Update baselines when UI changes are intentional
- ✅ Review diff reports when tests fail
- ✅ Follow best practices for stable tests

For more examples, see [Testing Examples](examples.md).
