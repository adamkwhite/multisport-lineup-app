# CI/CD Pipeline Documentation

## Overview

The baseball-lineup-app uses a **3-stage GitHub Actions pipeline** for comprehensive PR validation. Each stage builds on the previous, providing fast feedback while ensuring code quality.

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
│  Stage 2: Tests & SonarQube Analysis (2-3 minutes)          │
│  ✓ Python unit tests (pytest)                               │
│  ✓ JavaScript tests (Jest)                                  │
│  ✓ Code coverage (94%+ target)                              │
│  ✓ SonarQube quality gate                                   │
│  ✓ Verification step (outcome checks)                       │
└─────────────────────┬───────────────────────────────────────┘
                      │ PASS
                      ▼
┌─────────────────────────────────────────────────────────────┐
│  Stage 3: Claude Code Review (3-5 minutes)                  │
│  ✓ AI-powered code review                                   │
│  ✓ Best practices check                                     │
│  ✓ Security review                                          │
│  ✓ Automated feedback on PR                                 │
└─────────────────────────────────────────────────────────────┘
```

## Stage 1: Quick Validation

**Purpose:** Fast feedback on code style issues
**Duration:** 15-30 seconds
**Blocks:** Stages 2 and 3

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

## Stage 2: Tests & SonarQube Analysis

**Purpose:** Comprehensive testing and quality analysis
**Duration:** 2-3 minutes
**Blocks:** Stage 3
**Depends on:** Stage 1 passing

### Checks

1. **Python Tests**
   ```bash
   pytest tests/unit/ tests/edge_cases/ --cov=app --cov-report=xml --cov-report=term-missing
   ```
   - 150+ unit and edge case tests
   - 94%+ code coverage target
   - Coverage report sent to SonarQube

2. **JavaScript Tests**
   ```bash
   npm test -- --coverage --watchAll=false
   ```
   - Jest test suite
   - Coverage tracked

3. **SonarQube Scan**
   - Static code analysis
   - Security vulnerability detection
   - Code smell identification
   - Duplicated code detection

4. **SonarQube Quality Gate**
   - Must pass quality gate to proceed
   - Blocks merge if quality standards not met
   - Checks coverage, bugs, vulnerabilities, code smells

5. **Verification Step**
   - Explicitly checks all test outcomes
   - Redundant safety check
   - See `docs/development/ci-pipeline-safeguards.md`

## Stage 3: Claude Code Review

**Purpose:** AI-powered code review
**Duration:** 3-5 minutes
**Depends on:** Stage 2 passing

### Review Areas

- Code quality and best practices
- Potential bugs or issues
- Performance considerations
- Security concerns
- Test coverage adequacy

**Note:** Review comments are posted directly on the PR.

## Safeguards

The pipeline has **6 layers of safeguards** to ensure test failures always block the pipeline:

1. Global shell options (`-eo pipefail`)
2. Job-level `continue-on-error: false`
3. Step-level `continue-on-error: false`
4. No error suppression operators (`|| true`)
5. Explicit outcome verification
6. Job dependency chain with `if: success()`

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
SonarQube project configuration

## Environment Variables & Secrets

Required GitHub Secrets:
- `SONAR_TOKEN` - SonarQube authentication token
- `SONAR_HOST_URL` - SonarQube server URL (http://44.206.255.230:9000)
- `CLAUDE_CODE_OAUTH_TOKEN` - Claude Code API token

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
./baseball-venv/bin/pytest tests/unit/ tests/edge_cases/ --cov=app --cov-report=term-missing

# JavaScript tests
npm test -- --coverage
```

### SonarQube (optional)
```bash
# Requires SonarQube server access
sonar-scanner
```

## Failure Scenarios

### Stage 1 Fails
- **Symptom:** Red X on "Quick Validation"
- **Fix:** Run Black/isort/Flake8 locally and commit fixes
- **Impact:** Stages 2 and 3 skipped

### Stage 2 Fails - Tests
- **Symptom:** Red X on "Tests & SonarQube Analysis"
- **Fix:** Fix failing tests, verify locally with pytest
- **Impact:** Stage 3 skipped

### Stage 2 Fails - Quality Gate
- **Symptom:** Red X on "SonarQube Quality Gate Check"
- **Fix:** Address code quality issues reported in SonarQube
- **Impact:** Stage 3 skipped

### Stage 3 Fails
- **Symptom:** Claude review finds issues
- **Fix:** Address review comments
- **Impact:** Informational, doesn't block merge (but should be addressed)

## Performance

| Stage | Duration | Can Run in Parallel |
|-------|----------|---------------------|
| Stage 1 | 15-30s | No (sequential) |
| Stage 2 | 2-3 min | No (depends on Stage 1) |
| Stage 3 | 3-5 min | No (depends on Stage 2) |
| **Total** | **5-8 min** | N/A |

## Best Practices

1. **Run Stage 1 checks before pushing**
   - Saves CI time
   - Faster feedback loop

2. **Run tests locally before creating PR**
   - Catch failures early
   - Don't waste CI resources

3. **Address Claude review comments**
   - Even if they don't block merge
   - Improve code quality

4. **Monitor SonarQube dashboard**
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

### SonarQube quality gate fails
- View details: http://44.206.255.230:9000/dashboard?id=baseball-lineup-app
- Address reported issues
- Re-run pipeline

## Related Documentation

- [CI Pipeline Safeguards](./ci-pipeline-safeguards.md)
- [SonarQube Usage](./sonarqube-usage.md)
- [SonarQube Setup Guide](./sonarqube-setup-guide.md)
- [Testing Guidelines](../testing/guidelines.md)

## Maintenance

### Adding New Checks

1. Add to appropriate stage in `.github/workflows/pr-validation.yml`
2. Test locally first
3. Update this documentation
4. Consider impact on pipeline duration

### Modifying Quality Standards

- **Flake8 rules:** Update `--extend-ignore` in workflow
- **Coverage targets:** Update pytest and SonarQube configs
- **SonarQube rules:** Configure in SonarQube UI

### Pipeline Evolution

Current version: v1.0 (3-stage pipeline)

Future improvements:
- Parallel test execution
- Test result caching
- Selective test runs based on changed files
- Performance budgets
