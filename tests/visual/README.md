# Visual Regression Tests

Visual regression tests use Playwright to capture screenshots and detect UI changes.

## Prerequisites

1. Install Playwright browsers:
   ```bash
   ./baseball-venv/bin/playwright install chromium
   ```

2. Start the Flask app:
   ```bash
   ./start.sh
   ```
   Or:
   ```bash
   ./baseball-venv/bin/python app.py
   ```

## Running Visual Tests

Visual tests are skipped by default since they require the app to be running.

### Run all visual tests:
```bash
./baseball-venv/bin/pytest tests/visual/ -v --headed
```

### Run with test markers:
```bash
# Run without skip markers (force run)
./baseball-venv/bin/pytest tests/visual/ -v -m "not skip"
```

### Run specific test file:
```bash
./baseball-venv/bin/pytest tests/visual/test_visual_login.py -v --headed
```

### Run in headed mode (see browser):
```bash
./baseball-venv/bin/pytest tests/visual/ -v --headed --slowmo=1000
```

## Generating Baseline Screenshots

On first run, Playwright will generate baseline screenshots in:
```
tests/visual/*-snapshots/
```

These baselines should be committed to git for comparison.

## Updating Baselines

If UI changes are intentional, update baselines:

```bash
./baseball-venv/bin/pytest tests/visual/ --update-snapshots
```

Review the changes and commit updated baselines.

## Screenshot Organization

Screenshots are organized by test file:
```
tests/visual/
├── test_visual_login.py-snapshots/
│   ├── login-page-initial.png
│   ├── login-page-mobile.png
│   └── login-page-tablet.png
├── test_visual_dashboard.py-snapshots/
│   ├── dashboard-authenticated-demo.png
│   └── dashboard-no-auth.png
└── test_visual_lineup.py-snapshots/
    ├── lineup-9-players.png
    └── lineup-with-bench.png
```

## Troubleshooting

### Tests fail with "Application not running"
- Ensure Flask app is running on `http://localhost:5001`
- Check that port 5001 is not in use by another process

### Screenshots differ on different machines
- Use consistent viewport sizes (1280x720 default)
- Ensure same browser version
- Consider using Docker for consistent environment

### Flaky tests
- Add explicit waits: `page.wait_for_load_state("networkidle")`
- Use `page.wait_for_selector()` for dynamic content
- Increase timeout if needed: `page.set_default_timeout(30000)`

## Best Practices

1. **Wait for content**: Always wait for page to fully load
2. **Stable selectors**: Use data-testid attributes when possible
3. **Hide dynamic content**: Mock timestamps, random data
4. **Consistent viewport**: Use same size across tests
5. **Meaningful names**: Screenshot names should describe what they test

## CI/CD Integration

Visual tests can run in CI with headless mode:

```bash
pytest tests/visual/ --headed=false
```

Store baseline screenshots in git for CI comparison.
