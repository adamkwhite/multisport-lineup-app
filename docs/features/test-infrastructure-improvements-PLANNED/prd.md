# Product Requirements Document: Test Infrastructure Improvements

## Overview

Improve the test suite's maintainability, reliability, and adherence to pytest best practices by addressing three critical code quality issues identified during PR review: import path manipulation, brittle error message assertions, and test data dependencies.

## Problem Statement

The current test suite has several patterns that reduce maintainability and reliability:

1. **Import Path Manipulation**: Every test file contains duplicate `sys.path.insert()` boilerplate, making tests fragile and non-standard
2. **Brittle Error Assertions**: Tests check specific error message strings, causing test failures when messages are improved or translated
3. **Non-Deterministic Test Data**: Tests have conditional logic based on file existence, leading to inconsistent behavior across environments

These issues were identified in PR review feedback and need to be addressed to maintain the high test coverage (94%+) achieved in PR #31.

## Goals

### Primary Goals
- Eliminate duplicate import path manipulation from individual test files
- Implement error code system for all API responses
- Remove file dependencies from demo mode tests using fixtures

### Secondary Goals
- Establish patterns for future test development
- Maintain or improve current 94%+ test coverage
- Ensure all existing tests pass after refactoring

## User Stories

**As a developer**, I want test files to be clean and focused on test logic, so that I can quickly understand what each test validates without parsing boilerplate code.

**As a product manager**, I want to improve error messages without breaking tests, so that we can enhance user experience based on feedback without regression.

**As a CI/CD pipeline**, I want tests to behave identically across all environments, so that test results are reliable and trustworthy.

**As a new contributor**, I want to follow established testing patterns, so that I can write high-quality tests that match the project standards.

## Functional Requirements

### FR1: Centralized Import Configuration
1. The root `tests/conftest.py` shall contain the `sys.path.insert()` statement once
2. All individual test files shall remove their `sys.path.insert()` statements
3. Tests shall continue to import from `app` module successfully
4. The import pattern shall work for all test subdirectories (unit/, edge_cases/, visual/)

**Files affected:**
- `tests/unit/test_demo_mode.py` (line 11)
- `tests/unit/test_auth_routes.py` (line 11)
- `tests/unit/test_lineup_generation.py` (if applicable)
- `tests/unit/test_utility_functions.py` (if applicable)
- `tests/edge_cases/test_edge_case_*.py` (if applicable)
- `tests/visual/test_visual_*.py` (if applicable)

### FR2: Error Code System
1. All API error responses shall include both human-readable message and machine-readable code
2. Error codes shall use SCREAMING_SNAKE_CASE format (e.g., `TOKEN_EXCHANGE_ERROR`)
3. Error response format shall be: `{"error": "Human message", "code": "ERROR_CODE"}`
4. Test assertions shall check error codes instead of error message strings
5. A constants file (`app/constants.py`) shall define all error codes in one location

**Error codes to implement:**
- `NOT_AUTHENTICATED` - User not logged in
- `TOKEN_EXCHANGE_ERROR` - OAuth token exchange failed
- `AUTHENTICATION_FAILED` - Auth callback without code parameter
- `DEMO_DATA_UNAVAILABLE` - Demo data file missing or invalid
- Additional codes as needed for other API errors

**Files affected:**
- `app.py` - All API error responses
- `tests/unit/test_auth_routes.py` - Update assertions (lines 55, 85, 111, 118, 124)
- New file: `app/constants.py` - Error code definitions

### FR3: Mock Demo Data Fixtures
1. Create reusable pytest fixture for demo data in `tests/fixtures/demo_data.py`
2. Remove conditional test logic based on file existence
3. Use `monkeypatch` to inject mock data in tests
4. Fixture shall provide realistic demo data structure matching production format
5. Tests shall be deterministic and not depend on external files

**Files affected:**
- New file: `tests/fixtures/demo_data.py` - Demo data fixture
- `tests/unit/test_demo_mode.py` - Remove conditional logic (lines 48-58, 80-90, 97-107)
- Update all tests using `load_demo_data()` to use fixture

**Demo data structure:**
```python
{
    'team': {'id': str, 'name': str},
    'players': [{'id': str, 'name': str, ...}],
    'games': [{'id': str, 'date': str, ...}]
}
```

### FR4: Pattern Documentation
1. Update `docs/testing/guidelines.md` with new patterns
2. Document error code usage for future API endpoints
3. Document fixture usage for test data
4. Include code examples for each pattern

## Non-Goals (Out of Scope)

- Adding new test cases (coverage improvement is separate effort in PR #31)
- Refactoring non-test application code (only error response format changes)
- Implementing internationalization/translation system
- Changing HTTP status codes
- Modifying visual test logic beyond import cleanup
- Performance optimization of test suite

## Technical Considerations

### Existing Infrastructure
- Pytest is already configured with fixtures in `tests/conftest.py`
- Test coverage is 94%+ (from PR #31)
- Visual tests use Playwright and have separate conftest
- Tests use monkeypatch already (see `test_demo_mode.py:109-124`)

### Implementation Approach
1. **Phase 1**: Add error codes to app responses and constants file
2. **Phase 2**: Create demo data fixture
3. **Phase 3**: Update test assertions to use error codes
4. **Phase 4**: Update tests to use demo data fixture
5. **Phase 5**: Remove duplicate sys.path imports from test files
6. **Phase 6**: Update documentation

### Backward Compatibility
- Error responses will include both `error` (message) and `code` fields
- Existing error message assertions will be updated, not removed
- Frontend/API consumers can start using error codes immediately

### Dependencies
- No new package dependencies required
- Uses existing pytest, monkeypatch, and fixture capabilities
- Works with current Flask test client setup

## Success Criteria

### Validation Checklist
- [ ] All tests pass after refactoring (pytest exit code 0)
- [ ] Test coverage remains at 94%+ (measured by pytest-cov)
- [ ] No `sys.path.insert()` statements in individual test files
- [ ] All API error responses include `code` field
- [ ] All test assertions check error codes, not message strings
- [ ] No conditional test logic based on file existence in `test_demo_mode.py`
- [ ] Demo data fixture is used in all relevant tests
- [ ] `docs/testing/guidelines.md` updated with new patterns
- [ ] PR review passes without test infrastructure concerns

### Success Metrics
1. **Maintainability**: Error messages can be changed without test failures
2. **Reliability**: Tests produce identical results across all environments
3. **Clarity**: Test files contain only test logic, no boilerplate
4. **Standards**: Follows pytest best practices and community standards

## Acceptance Criteria

### For Issue #1: Import Path Manipulation
- Root `conftest.py` contains single `sys.path.insert()` statement
- Zero occurrences of `sys.path.insert()` in individual test files
- All tests successfully import from `app` module
- Pytest runs successfully from project root

### For Issue #2: Brittle Error Message Assertions
- `app/constants.py` exists with all error code definitions
- All API error responses include `code` field
- Zero test assertions checking `'string' in data['error']`
- All test assertions check `data['code'] == CONSTANT`

### For Issue #3: Test Data Dependency
- `tests/fixtures/demo_data.py` provides mock demo data fixture
- Zero occurrences of `if data is not None:` conditional test logic
- All demo mode tests use mocked data via monkeypatch
- Tests do not read from actual demo JSON files

## Open Questions

- Should error codes follow a specific namespace pattern (e.g., `AUTH_*`, `API_*`)?
- Should we add error code constants to frontend JavaScript for client-side handling?
- Do visual/Playwright tests need any special handling for the conftest changes?
- Should we add a test that validates all error codes are documented?

## Timeline

### Estimated Implementation: 4-6 hours

**Phase 1: Setup (1 hour)**
- Create `app/constants.py`
- Create `tests/fixtures/demo_data.py`
- Define all error codes

**Phase 2: Application Changes (1 hour)**
- Update all API error responses to include codes
- Update import statements in app.py if needed

**Phase 3: Test Updates (2-3 hours)**
- Update test assertions to use error codes
- Update demo mode tests to use fixtures
- Remove conditional test logic
- Remove duplicate sys.path imports

**Phase 4: Documentation & Validation (1 hour)**
- Update testing guidelines
- Run full test suite
- Fix any issues
- Verify coverage remains 94%+

## Related Work

- **PR #31**: Test coverage improvements (currently at 94%+)
- **Issue #22**: Code quality refactoring initiative
- **Issue #24**: Testing infrastructure improvements
- **Issue #33**: Remove duplicate sys.path manipulation from test files
- **Issue #34**: Replace brittle error message assertions with error codes
- **Issue #35**: Remove file dependencies from demo mode tests

## References

- PR Review Feedback: [multisport-lineup-app/pull/31](https://github.com/adamkwhite/multisport-lineup-app/pull/31)
- GitHub Issues: [#33](https://github.com/adamkwhite/multisport-lineup-app/issues/33), [#34](https://github.com/adamkwhite/multisport-lineup-app/issues/34), [#35](https://github.com/adamkwhite/multisport-lineup-app/issues/35)
- Pytest Best Practices: https://docs.pytest.org/en/stable/goodpractices.html
- Project Testing Guidelines: `docs/testing/guidelines.md`
