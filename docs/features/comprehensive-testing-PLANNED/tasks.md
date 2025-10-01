# Comprehensive Testing Strategy - Tasks

## Relevant Files

### Test Files (New)
- `tests/edge_cases/test_edge_case_lineup.py` - Edge cases for lineup generation
- `tests/edge_cases/test_edge_case_obfuscation.py` - Edge cases for name obfuscation
- `tests/edge_cases/test_edge_case_errors.py` - Error handling edge cases
- `tests/visual/test_visual_login.py` - Visual regression for login page
- `tests/visual/test_visual_dashboard.py` - Visual regression for dashboard
- `tests/visual/test_visual_lineup.py` - Visual regression for lineup display
- `tests/fixtures/player_data.py` - Reusable player test data
- `tests/fixtures/game_data.py` - Reusable game test data
- `tests/fixtures/session_helpers.py` - Session management helpers

### Documentation Files (New)
- `docs/testing/guidelines.md` - Testing philosophy and standards
- `docs/testing/examples.md` - Test examples for common patterns
- `docs/testing/visual-regression.md` - Playwright visual testing guide
- `docs/testing/troubleshooting.md` - Common test issues and solutions

### Configuration Files
- `requirements.txt` - Add pytest-playwright, pytest-mock
- `pytest.ini` - Update with coverage targets and test paths
- `playwright.config.py` - Playwright configuration for Python
- `.github/workflows/tests.yml` - Update to include visual tests (optional)

### Existing Files to Update
- `tests/test_utility_functions.py` - Add more edge cases
- `tests/test_lineup_generation.py` - Add constraint conflict tests
- `tests/test_auth_routes.py` - Add session edge cases
- `tests/test_demo_mode.py` - Add malformed data tests

## Tasks

### 1.0 Set up testing infrastructure and reorganize test structure
- [ ] 1.1 Create test directory structure (edge_cases/, visual/, fixtures/)
- [ ] 1.2 Install Playwright and pytest-playwright dependencies
- [ ] 1.3 Run `playwright install` to download browser binaries
- [ ] 1.4 Create playwright.config.py with browser and screenshot settings
- [ ] 1.5 Create tests/fixtures/__init__.py and common fixture files
- [ ] 1.6 Move existing tests to tests/unit/ subdirectory
- [ ] 1.7 Update pytest.ini with new test paths and 90% coverage target
- [ ] 1.8 Create tests/conftest.py with shared fixtures and Playwright setup

### 2.0 Add edge case tests for lineup generation logic
- [ ] 2.1 Create tests/edge_cases/test_edge_case_lineup.py file
- [ ] 2.2 Add test for exactly 9 players (no bench)
- [ ] 2.3 Add test for 10 players (minimal bench rotation)
- [ ] 2.4 Add test for 12 players (balanced bench rotation)
- [ ] 2.5 Add test for 15+ players (heavy bench rotation)
- [ ] 2.6 Add test for all players wanting same position (conflict)
- [ ] 2.7 Add test for impossible position constraints (e.g., no catchers)
- [ ] 2.8 Add test for single player with all positions restricted
- [ ] 2.9 Add test for must-play player logic (sat out 2+ lineups)
- [ ] 2.10 Add test for catcher rotation across multiple lineups
- [ ] 2.11 Add test for position history tracking and rotation
- [ ] 2.12 Verify coverage increase for generate_lineup() function

### 3.0 Add edge case tests for utility functions and error handling
- [ ] 3.1 Create tests/edge_cases/test_edge_case_obfuscation.py
- [ ] 3.2 Add test for obfuscate_name() with unicode characters (émoji, 中文)
- [ ] 3.3 Add test for obfuscate_name() with special chars (@, #, $)
- [ ] 3.4 Add test for obfuscate_name() with very long names (100+ chars)
- [ ] 3.5 Add test for obfuscate_name() with hyphenated names
- [ ] 3.6 Create tests/edge_cases/test_edge_case_errors.py
- [ ] 3.7 Add test for session expiration handling
- [ ] 3.8 Add test for missing session keys
- [ ] 3.9 Add test for concurrent session modifications
- [ ] 3.10 Add test for malformed JSON in request bodies
- [ ] 3.11 Add test for invalid team_id/game_id formats
- [ ] 3.12 Add test for load_demo_data() with corrupted JSON
- [ ] 3.13 Verify error handler coverage reaches 95%

### 4.0 Implement visual regression testing framework
- [ ] 4.1 Create tests/visual/ directory and __init__.py
- [ ] 4.2 Create tests/visual/conftest.py with Playwright page fixture
- [ ] 4.3 Create tests/visual/test_visual_login.py
- [ ] 4.4 Add test for login page initial state screenshot
- [ ] 4.5 Add test for demo mode button hover state
- [ ] 4.6 Create tests/visual/test_visual_dashboard.py
- [ ] 4.7 Add test for dashboard with no auth (login shown)
- [ ] 4.8 Add test for dashboard with auth (team selection shown)
- [ ] 4.9 Add test for empty states (no teams, no games, no players)
- [ ] 4.10 Create tests/visual/test_visual_lineup.py
- [ ] 4.11 Add test for lineup display with 9 players on field
- [ ] 4.12 Add test for lineup display with bench players shown
- [ ] 4.13 Add test for lineup display error state
- [ ] 4.14 Create baseline screenshots directory (tests/visual/screenshots/)
- [ ] 4.15 Run visual tests and generate baseline screenshots
- [ ] 4.16 Update .gitignore to track baseline but ignore test-results

### 5.0 Create comprehensive testing documentation
- [ ] 5.1 Create docs/testing/ directory
- [ ] 5.2 Create docs/testing/guidelines.md with testing philosophy
- [ ] 5.3 Add section on when to write unit vs integration vs visual tests
- [ ] 5.4 Add section on test naming conventions and file organization
- [ ] 5.5 Add section on using fixtures and avoiding duplication
- [ ] 5.6 Create docs/testing/examples.md
- [ ] 5.7 Add example: Testing a Flask route with mocked session
- [ ] 5.8 Add example: Testing utility function with edge cases
- [ ] 5.9 Add example: Testing error handler with exception
- [ ] 5.10 Add example: Using test fixtures for player data
- [ ] 5.11 Add example: Writing Playwright visual regression test
- [ ] 5.12 Create docs/testing/visual-regression.md
- [ ] 5.13 Document Playwright setup and browser configuration
- [ ] 5.14 Document how to run visual tests locally
- [ ] 5.15 Document how to update baseline screenshots
- [ ] 5.16 Document troubleshooting flaky visual tests
- [ ] 5.17 Create docs/testing/troubleshooting.md
- [ ] 5.18 Add common test failures and solutions
- [ ] 5.19 Add debugging tips for failed assertions
- [ ] 5.20 Add performance optimization tips for slow tests

### 6.0 Optimize and validate test coverage to reach 90%
- [ ] 6.1 Run pytest with coverage report and identify uncovered lines
- [ ] 6.2 Add tests for any uncovered utility functions
- [ ] 6.3 Add tests for production-specific code paths (if testable)
- [ ] 6.4 Review and add tests for implicit else branches
- [ ] 6.5 Add tests for rarely-hit error conditions
- [ ] 6.6 Run full test suite and ensure all tests pass (unit + visual)
- [ ] 6.7 Verify total test execution time is under 10 seconds (unit tests)
- [ ] 6.8 Generate final coverage report showing 90%+ for app.py
- [ ] 6.9 Update README.md with testing instructions
- [ ] 6.10 Create PR with all testing improvements

## Progress Tracking

- **Phase 1 (Edge Case Testing)**: Tasks 1.0, 2.0, 3.0 - Target: 75% coverage
- **Phase 2 (Visual Regression)**: Task 4.0 - Adds visual safety net
- **Phase 3 (Documentation)**: Task 5.0 - Enables contributors
- **Phase 4 (Refinement)**: Task 6.0 - Achieves 90% target

## Notes

- Playwright MCP is installed and ready to use
- All visual tests use Playwright (no Puppeteer)
- Visual tests should run headless in CI
- Focus on high-value tests that prevent real bugs
- Document any code intentionally left untested (e.g., production-only startup code)
- Keep unit tests fast - visual tests can be slower
