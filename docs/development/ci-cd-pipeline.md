# CI/CD Pipeline Documentation

## Overview

The multisport-lineup-app uses a **2-stage GitHub Actions pipeline** for comprehensive PR validation. Each stage builds on the previous, providing fast feedback while ensuring code quality.

**Pipeline File:** `.github/workflows/pr-validation.yml`

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  PR Created/Updated                                          │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Stage 1: Quick Validation (15-30 seconds)                   │
│  ✓ Black code formatting                                     │
│  ✓ isort import sorting                                      │
│  ✓ Flake8 linting                                           │
└─────────────────────┬───────────────────────────────────────┘
                      │ PASS
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Stage 2: Tests & SonarCloud Analysis (2-3 minutes)         │
│  ✓ Python unit tests (pytest)                               │
│  ✓ JavaScript tests (Jest)                                  │
│  ✓ Code coverage (94%+ target)                              │
│  ✓ SonarCloud quality gate (80%+ new code coverage)         │
│  ✓ Verification step (outcome checks)                       │
└─────────────────────────────────────────────────────────────┘
```

## Stage 1: Quick Validation

**Purpose:** Fast feedback on code style issues
**Duration:** 15-30 seconds
**Blocks:** Stage 2

### Checks

1. **Black** - Code formatting
   ```bash
   black --check app.py tests/
   ```

2. **isort** - Import sorting (Black-compatible profile)
   ```bash
   isort --check-only app.py tests/
   ```

3. **Flake8** - Code linting
   ```bash
   flake8 app.py tests/ --max-line-length=100 --extend-ignore=E203,W503,E402,F401,F841,F811,E501,F541
   ```

### Why This Stage Exists

- Provides immediate feedback on trivial issues
- Prevents wasting CI time on formatting failures
- Developers fix style issues before running expensive tests

## Stage 2: Tests & SonarCloud Analysis

**Purpose:** Comprehensive testing and quality analysis
**Duration:** 2-3 minutes
**Depends on:** Stage 1 passing

### Checks

1. **Python Tests**
   ```bash
   pytest tests/unit/ tests/edge_cases/ --cov=app --cov-report=xml --cov-report=term-missing
   ```
   - 150+ unit and edge case tests
   - 94%+ code coverage target
   - Coverage report sent to SonarCloud

2. **JavaScript Tests**
   ```bash
   npm test -- --coverage --watchAll=false
   ```
   - Jest test suite
   - Coverage tracked

3. **SonarCloud Scan**
   - Static code analysis
   - Security vulnerability detection
   - Code smell identification
   - Duplicated code detection
   - Public dashboard: https://sonarcloud.io/project/overview?id=adamkwhite_multisport-lineup-app

4. **SonarCloud Quality Gate ("Sonar way" default)**
   - Must pass quality gate to proceed
   - Blocks merge if quality standards not met
   - New code coverage ≥ 80%
   - Checks bugs, vulnerabilities, code smells, security hotspots

5. **Verification Step**
   - Explicitly checks all test outcomes
   - Redundant safety check
   - See `docs/development/ci-pipeline-safeguards.md`

## Safeguards

The pipeline has **5 layers of safeguards** to ensure test failures always block the pipeline:

1. Global shell options (`-eo pipefail`)
2. Job-level `continue-on-error: false`
3. Step-level `continue-on-error: false`
4. No error suppression operators (`|| true`)
5. Explicit outcome verification

**Full documentation:** `docs/development/ci-pipeline-safeguards.md`

## Configuration Files

### `.github/workflows/pr-validation.yml`
Main pipeline definition

### `.isort.cfg`
```ini
[settings]
profile = black
```
Ensures isort and Black don't conflict

### `pytest.ini`
Test configuration (coverage, markers, etc.)

### `sonar-project.properties`
SonarCloud project configuration
- Project key: `adamkwhite_multisport-lineup-app`
- Organization: `adamkwhite`

## Environment Variables & Secrets

Required GitHub Secrets:
- `SONAR_TOKEN` - SonarCloud authentication token

## Running Locally

### Quick Validation (Stage 1)
```bash
# Format code
python3 -m venv venv
venv/bin/pip install black isort flake8
venv/bin/black app.py tests/
venv/bin/isort app.py tests/
venv/bin/flake8 app.py tests/ --max-line-length=100 --extend-ignore=E203,W503,E402,F401,F841,F811,E501,F541
```

### Tests (Stage 2)
```bash
# Python tests
./lineup-venv/bin/pytest tests/unit/ tests/edge_cases/ --cov=app --cov-report=term-missing

# JavaScript tests
npm test -- --coverage
```

### SonarCloud (optional)
```bash
# Requires SonarCloud account and SONAR_TOKEN
# View results at: https://sonarcloud.io/project/overview?id=adamkwhite_multisport-lineup-app
sonar-scanner
```

## Failure Scenarios

### Stage 1 Fails
- **Symptom:** Red X on "Quick Validation"
- **Fix:** Run Black/isort/Flake8 locally and commit fixes
- **Impact:** Stage 2 skipped

### Stage 2 Fails - Tests
- **Symptom:** Red X on "Tests & SonarCloud Analysis"
- **Fix:** Fix failing tests, verify locally with pytest

### Stage 2 Fails - Quality Gate
- **Symptom:** Red X on "SonarCloud Quality Gate Check"
- **Fix:** Address code quality issues reported in SonarCloud dashboard
- **Dashboard:** https://sonarcloud.io/project/overview?id=adamkwhite_multisport-lineup-app

## Performance

| Stage | Duration | Can Run in Parallel |
|-------|----------|---------------------|
| Stage 1 | 15-30s | No (sequential) |
| Stage 2 | 2-3 min | No (depends on Stage 1) |
| **Total** | **2.5-3.5 min** | N/A |

## Best Practices

1. **Run Stage 1 checks before pushing**
   - Saves CI time
   - Faster feedback loop

2. **Run tests locally before creating PR**
   - Catch failures early
   - Don't waste CI resources

3. **Monitor SonarCloud dashboard**
   - Public dashboard: https://sonarcloud.io/project/overview?id=adamkwhite_multisport-lineup-app
   - Track technical debt
   - Improve code quality over time

## Troubleshooting

### "Black would reformat" errors
```bash
# Fix locally
venv/bin/black app.py tests/
git add -u
git commit -m "Fix formatting"
```

### "isort would reformat" errors
```bash
# Fix locally
venv/bin/isort app.py tests/
git add -u
git commit -m "Fix import sorting"
```

### Tests pass locally but fail in CI
- Check Python version (CI uses 3.12)
- Check for environment-specific issues
- Review CI logs for differences

### SonarCloud quality gate fails
- View details: https://sonarcloud.io/project/overview?id=adamkwhite_multisport-lineup-app
- Check "New Code" tab for issues
- Address reported issues (coverage, bugs, vulnerabilities, code smells)
- Re-run pipeline

## Related Documentation

- [CI Pipeline Safeguards](./ci-pipeline-safeguards.md)
- [SonarCloud Dashboard](https://sonarcloud.io/project/overview?id=adamkwhite_multisport-lineup-app) (public)
- [Testing Guidelines](../testing/guidelines.md)

## Maintenance

### Adding New Checks

1. Add to appropriate stage in `.github/workflows/pr-validation.yml`
2. Test locally first
3. Update this documentation
4. Consider impact on pipeline duration

### Modifying Quality Standards

- **Flake8 rules:** Update `--extend-ignore` in workflow
- **Coverage targets:** Update pytest config (local) and SonarCloud quality gate (cloud)
- **SonarCloud rules:** Configure in SonarCloud UI (Quality Gates tab)

### Pipeline Evolution

Current version: v2.0 (2-stage pipeline)

Future improvements:
- Parallel test execution
- Test result caching
- Selective test runs based on changed files
- Performance budgets
