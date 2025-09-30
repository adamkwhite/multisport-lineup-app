# SonarQube Integration - Usage Guide

## Overview

The Baseball Lineup App integrates with SonarQube for continuous code quality monitoring and analysis. SonarQube automatically scans code on every PR and push to main, providing quality metrics, security analysis, and coverage tracking.

**SonarQube Dashboard:** http://44.206.255.230:9000/dashboard?id=baseball-lineup-app

## Quality Metrics

The project tracks 11 key quality metrics visible in the README badges:

1. **Quality Gate Status** - Overall pass/fail status
2. **Coverage** - Test coverage percentage
3. **Bugs** - Number of bug-level issues
4. **Vulnerabilities** - Security vulnerabilities found
5. **Code Smells** - Maintainability issues
6. **Security Rating** - A-E security rating
7. **Maintainability Rating** - A-E maintainability rating
8. **Reliability Rating** - A-E reliability rating
9. **Lines of Code** - Total lines analyzed
10. **Duplicated Lines** - Percentage of duplicate code
11. **Technical Debt** - Estimated time to fix all issues

## Development Workflow

### When You Create a PR

1. **Push your branch** to GitHub
2. **Create a pull request** to main
3. **GitHub Actions automatically**:
   - Runs Python tests with pytest (coverage reported to coverage.xml)
   - Runs JavaScript tests with Jest (coverage reported to lcov.info)
   - Sends code and coverage to SonarQube for analysis
   - Checks quality gate status
4. **PR status check** shows SonarQube scan result
5. **PR is blocked** if quality gate fails

### Quality Gate Thresholds

- **Python Coverage:** 80%+ for new code
- **JavaScript Coverage:** 85%+ for new code
- **Duplications:** Low duplicate code
- **Security:** No security hotspots or vulnerabilities
- **Maintainability:** Clean code with minimal code smells

### Viewing Results

**In GitHub PR:**
- Check the "SonarQube Scan" status in the PR checks
- Click to view full analysis in SonarQube

**In SonarQube Dashboard:**
- Visit: http://44.206.255.230:9000/dashboard?id=baseball-lineup-app
- View detailed metrics, issues, and coverage
- Drill down into specific files and issues

## Running Tests Locally

### Python Tests with Coverage

```bash
# Activate virtual environment
source baseball-venv/bin/activate

# Run pytest with coverage
pytest tests/api/ --cov=app --cov-report=xml:coverage.xml --cov-report=html --cov-report=term-missing

# View coverage report
open htmlcov/index.html
```

### JavaScript Tests with Coverage

```bash
# Run Jest with coverage
npm test -- --coverage

# View coverage report
open test-results/coverage-*/index.html
```

### Run All Tests (Organized Results)

```bash
# Use the test runner script
python scripts/run-tests.py

# This creates timestamped results and copies coverage files for SonarQube
```

## Configuration Files

### SonarQube Project Configuration

**File:** `sonar-project.properties`

```properties
sonar.projectKey=baseball-lineup-app
sonar.python.version=3.12
sonar.python.coverage.reportPaths=coverage.xml
sonar.javascript.lcov.reportPaths=lcov.info
sonar.sources=.
sonar.exclusions=**/*test*/**,**/__pycache__/**,baseball-venv/**,venv/**,htmlcov/**,test-results/**,scripts/**,docs/**,ai-dev-tasks/**,node_modules/**,*.pem,*.png,*.jpg,*.jpeg,*.gif
sonar.test.inclusions=tests/**/*.test.js,tests/**/*.py
sonar.coverage.exclusions=tests/**,**/*test*/**,scripts/**,docs/**,ai-dev-tasks/**
```

### GitHub Actions Workflow

**File:** `.github/workflows/sonarqube.yml`

Triggers on:
- Push to main branch
- Pull requests to main branch

Steps:
1. Checkout code
2. Set up Python 3.12
3. Set up Node.js 18
4. Install dependencies (Python and Node.js)
5. Run tests with coverage
6. Run SonarQube scan
7. Check quality gate (fails PR if quality gate fails)

## Troubleshooting

See [sonarqube-troubleshooting.md](sonarqube-troubleshooting.md) for common issues and solutions.

## Maintenance

### Updating Quality Gate Thresholds

1. Log into SonarQube: http://44.206.255.230:9000
2. Navigate to Project Settings > Quality Gates
3. Adjust thresholds as needed
4. Changes apply to future analyses

### Updating Exclusions

Edit `sonar-project.properties` to add/remove excluded paths:

```properties
sonar.exclusions=**/*test*/**,your/new/path/**
```

### GitHub Secrets

Required secrets (configured in repository settings):
- `SONAR_TOKEN` - SonarQube authentication token
- `SONAR_HOST_URL` - SonarQube instance URL (http://44.206.255.230:9000)

## Best Practices

1. **Fix issues before merging** - Address SonarQube findings in your PR
2. **Maintain coverage** - Add tests for new code to meet coverage thresholds
3. **Review security hotspots** - Check all security-related findings
4. **Monitor technical debt** - Keep debt ratio low by fixing code smells
5. **Use SonarQube feedback** - Learn from code quality suggestions

## Resources

- **Project Dashboard:** http://44.206.255.230:9000/dashboard?id=baseball-lineup-app
- **SonarQube Documentation:** https://docs.sonarqube.org/
- **PRD:** [prd-sonarqube-integration.md](prd-sonarqube-integration.md)
- **Task List:** [sonarqube-integration-tasks.md](sonarqube-integration-tasks.md)