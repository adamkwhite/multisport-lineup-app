# Comprehensive Testing Strategy - PRD

## Overview

Improve test coverage from current 60% to 90% for app.py by adding edge case testing, visual regression tests, and establishing testing guidelines for future development. This initiative will ensure code quality, prevent regressions, and provide clear testing patterns for contributors.

## Problem Statement

While recent improvements brought app.py coverage from 11% to 60%, significant gaps remain:
- 40% of app.py is untested (198 lines)
- Edge cases and error conditions lack coverage
- No visual regression testing for UI components
- No standardized testing guidelines for contributors
- Potential for UI regressions when modifying frontend code

Without comprehensive testing:
- Bugs may be introduced during refactoring
- Edge cases can cause production failures
- UI changes may break existing functionality
- New contributors lack clear testing patterns

## Goals

### Primary Goals
1. Achieve 90% test coverage for app.py
2. Implement visual regression testing for critical UI components
3. Create comprehensive testing guidelines and examples
4. Test all edge cases and error conditions

### Secondary Goals
1. Document testing patterns for future features
2. Establish maintainable test structure
3. Improve test execution speed where possible

## Success Criteria

- [x] app.py test coverage reaches 90% (currently 60%)
- [x] All identified edge cases have corresponding tests
- [x] Visual regression tests implemented for key UI screens
- [x] Testing guidelines document created
- [x] Test examples provided for common patterns
- [x] All tests pass in CI/CD pipeline
- [x] Test execution time remains under 10 seconds

## Requirements

### Functional Requirements

#### 1. Edge Case Testing
1.1. Test all error handling paths in app.py
1.2. Test boundary conditions (empty lists, max values, null/undefined)
1.3. Test concurrent session scenarios
1.4. Test malformed API responses
1.5. Test network failure scenarios
1.6. Test edge cases in lineup generation:
   - More players than positions
   - Exactly 9 players
   - Players with conflicting position constraints
   - All players restricted to same position
1.7. Test obfuscation with special characters and unicode
1.8. Test date/time edge cases (timezone boundaries, far future/past dates)

#### 2. Visual Regression Testing
2.1. Implement visual regression testing framework
2.2. Create baseline screenshots for:
   - Login page
   - Dashboard (authenticated)
   - Team selection screen
   - Game selection screen
   - Lineup display with full 9 players
   - Lineup display with bench players
   - Empty states (no teams, no games, no players)
   - Error states
2.3. Automated visual diff detection
2.4. Screenshot comparison in CI/CD pipeline

#### 3. Testing Guidelines
3.1. Document testing philosophy and standards
3.2. Provide unit test examples for:
   - Flask routes
   - Utility functions
   - Error handling
   - Session management
3.3. Provide visual regression test examples
3.4. Document how to run tests locally
3.5. Document how to add tests for new features
3.6. Include troubleshooting guide for common test failures

#### 4. Test Structure Improvements
4.1. Organize tests by concern (routes, utilities, business logic)
4.2. Create reusable test fixtures and helpers
4.3. Add test data factories for common scenarios
4.4. Document test file naming conventions

### Technical Requirements

1. Use pytest for Python unit tests (already in place)
2. Use Percy, Playwright, or similar for visual regression testing
3. Maintain test execution time under 10 seconds for unit tests
4. Visual regression tests should run in CI but not block local development
5. Tests must be deterministic (no flaky tests)
6. Coverage reports should be generated automatically
7. All test files should follow project structure conventions

### Non-Functional Requirements

1. Tests should be readable and self-documenting
2. Test code should follow same quality standards as production code
3. Tests should be maintainable (avoid brittle selectors, magic numbers)
4. Documentation should be beginner-friendly
5. Visual regression tests should handle responsive layouts

## User Stories

### As a Developer
- I want comprehensive edge case tests so that I can refactor code confidently
- I want visual regression tests so that I know my changes don't break the UI
- I want testing guidelines so that I know how to write good tests
- I want test examples so that I can quickly test new features correctly

### As a Maintainer
- I want 90% coverage so that the codebase is reliable and maintainable
- I want clear testing patterns so that contributors follow best practices
- I want automated visual testing so that UI regressions are caught early

### As a Contributor
- I want testing documentation so that I can add tests for my features
- I want reusable test fixtures so that I can write tests efficiently
- I want clear examples so that I understand the project's testing style

## Design Considerations

### Visual Regression Testing Tool Selection
- **Percy**: SaaS solution, good GitHub integration, free tier available
- **Playwright**: Open source, full control, requires screenshot storage
- **BackstopJS**: Open source, simple setup, good for basic needs

Recommended: **Playwright** for full control and no external dependencies

### Testing Documentation Structure
```
docs/
├── testing/
│   ├── guidelines.md          # Testing philosophy and standards
│   ├── examples.md             # Code examples for common patterns
│   ├── visual-regression.md    # Visual testing setup and usage
│   └── troubleshooting.md      # Common issues and solutions
```

### Test Organization
```
tests/
├── unit/                       # Pure unit tests (existing)
│   ├── test_utility_functions.py
│   ├── test_auth_routes.py
│   ├── test_demo_mode.py
│   └── test_lineup_generation.py
├── edge_cases/                 # Edge case scenarios (new)
│   ├── test_edge_case_lineup.py
│   ├── test_edge_case_obfuscation.py
│   └── test_edge_case_errors.py
├── visual/                     # Visual regression tests (new)
│   ├── test_visual_login.py
│   ├── test_visual_dashboard.py
│   └── test_visual_lineup.py
└── fixtures/                   # Shared test data (new)
    ├── player_data.py
    ├── game_data.py
    └── session_helpers.py
```

## Technical Specifications

### Coverage Targets by Module
- `obfuscate_name()`: 100% (simple utility)
- `can_fill_all_positions()`: 100% (critical business logic)
- `assign_positions_smart()`: 95% (complex algorithm, some paths rare)
- Route handlers: 85% (exclude production-only code)
- Error handlers: 95% (critical for reliability)
- Overall app.py: 90% (target)

### Visual Regression Test Example
```python
from playwright.sync_api import Page, expect

def test_dashboard_visual_regression(page: Page, authenticated_session):
    """Visual regression test for dashboard layout"""
    page.goto("http://localhost:5001/")

    # Wait for content to load
    page.wait_for_selector("[data-testid='team-list']")

    # Take screenshot
    screenshot = page.screenshot()

    # Compare with baseline (using Percy/Playwright)
    expect(page).to_have_screenshot("dashboard-authenticated.png")
```

### Edge Case Test Example
```python
def test_lineup_generation_conflicting_constraints(client):
    """Test lineup generation when constraints are impossible to satisfy"""
    payload = {
        'players': [
            {'id': i, 'name': f'Player {i}', 'position_preferences': [1]}
            for i in range(1, 10)  # All want to pitch
        ]
    }

    response = client.post('/api/lineup/generate', json=payload)

    # Should handle gracefully - either error or fallback assignment
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        data = response.get_json()
        # Verify fallback behavior
        assert len(data['lineups']) > 0
```

## Dependencies

### External Dependencies
- Playwright (or selected visual regression tool)
- pytest-playwright (if using Playwright)
- pytest-mock (for advanced mocking)

### Internal Dependencies
- Existing pytest setup
- Flask test client
- Current test fixtures

## Timeline

### Phase 1: Edge Case Testing (Week 1)
- Add edge case tests for lineup generation
- Add edge case tests for obfuscation
- Add error handling tests
- Target: Increase coverage to 75%

### Phase 2: Visual Regression Setup (Week 1-2)
- Select and configure visual regression tool
- Create baseline screenshots
- Add visual tests for critical screens
- Integrate with CI/CD

### Phase 3: Documentation (Week 2)
- Write testing guidelines
- Create test examples
- Document visual regression workflow
- Create troubleshooting guide

### Phase 4: Refinement (Week 2-3)
- Add remaining edge cases
- Optimize test performance
- Review and improve test organization
- Target: Achieve 90% coverage

## Risks and Mitigation

| Risk | Mitigation |
|------|------------|
| Visual tests are flaky | Use stable selectors, add explicit waits, test in consistent environment |
| Coverage target is unrealistic | Focus on high-value tests first, document why some code is intentionally untested |
| Tests slow down development | Keep unit tests fast (<10s), run visual tests only in CI |
| Test maintenance burden | Use fixtures and helpers to reduce duplication, document patterns clearly |
| Visual regression tool costs | Use open-source option (Playwright) or free tier (Percy) |

## Out of Scope

### Explicitly Not Included
- Integration tests with live TeamSnap API (deferred)
- Performance/load testing (future enhancement)
- Security penetration testing (separate initiative)
- Mobile-specific visual regression tests (responsive tests cover this)
- Automated test generation (manual test writing preferred)

### Future Considerations
- API integration testing when TeamSnap staging environment available
- Performance benchmarks for lineup generation
- Mutation testing for test quality assessment

## Acceptance Criteria

### Coverage Criteria
- [ ] app.py coverage is at least 90%
- [ ] All functions have at least one test
- [ ] All error paths are tested
- [ ] Coverage report shows detailed line-by-line coverage

### Edge Case Criteria
- [ ] Lineup generation tested with 9, 10, 12, 15 players
- [ ] Position constraint conflicts tested (impossible assignments)
- [ ] Empty/null inputs tested for all functions
- [ ] Unicode and special characters tested in obfuscation
- [ ] Date/time boundary conditions tested
- [ ] Session edge cases tested (expired, missing, concurrent)

### Visual Regression Criteria
- [ ] Visual tests exist for all major screens (7+ screens)
- [ ] Baseline screenshots captured and committed
- [ ] Visual diffs detected and reported in CI
- [ ] Tests pass on clean builds
- [ ] Documentation explains how to update baselines

### Documentation Criteria
- [ ] Testing guidelines document complete with philosophy and standards
- [ ] At least 5 test examples provided (routes, utilities, edge cases, visual, fixtures)
- [ ] Visual regression setup guide complete
- [ ] Troubleshooting guide covers common issues
- [ ] All documentation reviewed for clarity and accuracy

### Quality Criteria
- [ ] All tests pass locally and in CI
- [ ] No flaky tests (pass 10/10 times)
- [ ] Test execution time meets targets (unit <10s)
- [ ] Test code follows project conventions
- [ ] Tests are readable and well-documented

## Open Questions

1. Which visual regression tool should we use? (Recommendation: Playwright for full control)
2. Should visual tests block PRs or be informational only? (Recommendation: Informational initially, blocking after stabilization)
3. How should we handle baseline screenshot updates? (Recommendation: PR-based workflow with visual diffs shown)
4. Should we test dark mode variations? (Recommendation: Not initially, add if dark mode is implemented)

## Next Steps

After PRD approval:
1. Use generate-tasks.mdc to break down into implementation tasks
2. Use process-task-list.mdc to track progress
3. Create feature branch for implementation
4. Implement in phases as outlined in Timeline
