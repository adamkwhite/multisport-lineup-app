# SonarQube Integration Setup Guide

A comprehensive, step-by-step guide for integrating SonarQube code quality analysis into any GitHub repository.

## Overview

This guide walks through setting up automated SonarQube scanning with GitHub Actions, including quality gates, coverage tracking, and README badges.

**Time Required:** 30-60 minutes
**Prerequisites:** GitHub repository, SonarQube instance access

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Phase 1: Basic Configuration](#phase-1-basic-configuration)
3. [Phase 2: Test Coverage Infrastructure](#phase-2-test-coverage-infrastructure)
4. [Phase 3: GitHub Actions Workflow](#phase-3-github-actions-workflow)
5. [Phase 4: SonarQube Project Setup](#phase-4-sonarqube-project-setup)
6. [Phase 5: Validation](#phase-5-validation)
7. [Customization](#customization)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Information

Before starting, gather:
- **SonarQube Instance URL** (e.g., `http://your-sonarqube.com:9000`)
- **SonarQube Authentication Token** (generate from SonarQube → Account → Security → Generate Tokens)
- **Project Key** (kebab-case name, e.g., `my-awesome-app`)
- **Programming Languages** (Python, JavaScript, TypeScript, Java, etc.)
- **Test Framework(s)** (pytest, Jest, JUnit, etc.)

### Access Requirements

- Admin access to GitHub repository
- Access to SonarQube instance
- Ability to create GitHub Secrets

---

## Phase 1: Basic Configuration

### Step 1.1: Create `sonar-project.properties`

Create in repository root:

```properties
# Basic Configuration
sonar.projectKey=YOUR-PROJECT-KEY
sonar.python.version=3.12  # Adjust for your Python version
sonar.sources=.

# Coverage Reports (adjust for your stack)
sonar.python.coverage.reportPaths=coverage.xml
sonar.javascript.lcov.reportPaths=lcov.info

# Exclusions (customize for your project)
sonar.exclusions=**/*test*/**,**/__pycache__/**,**/venv/**,**/node_modules/**,**/htmlcov/**,**/test-results/**,**/coverage/**,**/scripts/**,**/docs/**,**/*.pem,**/*.png,**/*.jpg,**/*.jpeg,**/*.gif

# Test Configuration
sonar.tests=tests
sonar.test.inclusions=tests/**/*.test.js,tests/**/*.py
sonar.coverage.exclusions=tests/**,**/*test*/**,scripts/**,docs/**
```

**Customization points:**
- Replace `YOUR-PROJECT-KEY` with your kebab-case project name
- Adjust `sonar.python.version` to match your version
- Modify `sonar.sources` if code is in specific directories (e.g., `app,static`)
- Add/remove coverage report paths based on your languages
- Update exclusions to match your project structure

### Step 1.2: Update `.gitignore`

Add SonarQube working directory:

```gitignore
# SonarQube
.scannerwork/
```

### Step 1.3: Add README Badges

Add to top of `README.md` (update URL and project key):

```markdown
[![Quality Gate Status](http://YOUR-SONARQUBE-URL/api/project_badges/measure?project=YOUR-PROJECT-KEY&metric=alert_status)](http://YOUR-SONARQUBE-URL/dashboard?id=YOUR-PROJECT-KEY)
[![Coverage](http://YOUR-SONARQUBE-URL/api/project_badges/measure?project=YOUR-PROJECT-KEY&metric=coverage)](http://YOUR-SONARQUBE-URL/dashboard?id=YOUR-PROJECT-KEY)
[![Bugs](http://YOUR-SONARQUBE-URL/api/project_badges/measure?project=YOUR-PROJECT-KEY&metric=bugs)](http://YOUR-SONARQUBE-URL/dashboard?id=YOUR-PROJECT-KEY)
[![Vulnerabilities](http://YOUR-SONARQUBE-URL/api/project_badges/measure?project=YOUR-PROJECT-KEY&metric=vulnerabilities)](http://YOUR-SONARQUBE-URL/dashboard?id=YOUR-PROJECT-KEY)
[![Code Smells](http://YOUR-SONARQUBE-URL/api/project_badges/measure?project=YOUR-PROJECT-KEY&metric=code_smells)](http://YOUR-SONARQUBE-URL/dashboard?id=YOUR-PROJECT-KEY)
[![Security Rating](http://YOUR-SONARQUBE-URL/api/project_badges/measure?project=YOUR-PROJECT-KEY&metric=security_rating)](http://YOUR-SONARQUBE-URL/dashboard?id=YOUR-PROJECT-KEY)
[![Maintainability Rating](http://YOUR-SONARQUBE-URL/api/project_badges/measure?project=YOUR-PROJECT-KEY&metric=sqale_rating)](http://YOUR-SONARQUBE-URL/dashboard?id=YOUR-PROJECT-KEY)
[![Reliability Rating](http://YOUR-SONARQUBE-URL/api/project_badges/measure?project=YOUR-PROJECT-KEY&metric=reliability_rating)](http://YOUR-SONARQUBE-URL/dashboard?id=YOUR-PROJECT-KEY)
[![Lines of Code](http://YOUR-SONARQUBE-URL/api/project_badges/measure?project=YOUR-PROJECT-KEY&metric=ncloc)](http://YOUR-SONARQUBE-URL/dashboard?id=YOUR-PROJECT-KEY)
[![Duplicated Lines (%)](http://YOUR-SONARQUBE-URL/api/project_badges/measure?project=YOUR-PROJECT-KEY&metric=duplicated_lines_density)](http://YOUR-SONARQUBE-URL/dashboard?id=YOUR-PROJECT-KEY)
[![Technical Debt](http://YOUR-SONARQUBE-URL/api/project_badges/measure?project=YOUR-PROJECT-KEY&metric=sqale_index)](http://YOUR-SONARQUBE-URL/dashboard?id=YOUR-PROJECT-KEY)
```

---

## Phase 2: Test Coverage Infrastructure

### For Python Projects (pytest)

#### Step 2.1: Add Dependencies

Add to `requirements.txt`:
```
pytest==7.4.3
pytest-cov==4.1.0
```

#### Step 2.2: Create `pytest.ini`

```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --cov=app --cov-report=xml --cov-report=html --cov-report=term-missing --cov-fail-under=80
```

**Customize:**
- `--cov=app` → Replace `app` with your main package name
- `--cov-fail-under=80` → Adjust coverage threshold

### For JavaScript/TypeScript Projects (Jest)

#### Step 2.3: Add Dependencies

Add to `package.json`:
```json
{
  "devDependencies": {
    "jest": "^29.7.0",
    "@testing-library/jest-dom": "^6.1.4",
    "jest-environment-jsdom": "^29.7.0"
  },
  "scripts": {
    "test": "jest",
    "test:coverage": "jest --coverage"
  }
}
```

#### Step 2.4: Create `jest.config.js`

```javascript
module.exports = {
  testEnvironment: 'jsdom',
  collectCoverage: true,
  coverageDirectory: 'coverage',
  coverageReporters: ['text', 'lcov', 'html', 'cobertura'],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 85,
      lines: 85,
      statements: 85
    }
  },
  testMatch: ['**/tests/**/*.test.js'],
  testPathIgnorePatterns: [
    '<rootDir>/node_modules/',
    '<rootDir>/venv/'
  ]
};
```

**Customize:**
- Adjust `coverageThreshold` percentages
- Update `testMatch` pattern for your test file locations

---

## Phase 3: GitHub Actions Workflow

### Step 3.1: Create Workflow File

Create `.github/workflows/sonarqube.yml`:

```yaml
name: SonarQube Analysis

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  sonarqube:
    name: SonarQube Scan
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Shallow clones should be disabled for better analysis

      # Python Setup (skip if not needed)
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'  # Adjust version

      # Node.js Setup (skip if not needed)
      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'  # Adjust version

      # Python Dependencies (skip if not needed)
      - name: Install Python dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      # Node.js Dependencies (skip if not needed)
      - name: Install Node.js dependencies
        run: |
          npm install

      # Python Tests (skip if not needed)
      - name: Run Python tests with coverage
        run: |
          pytest --cov=app --cov-report=xml:coverage.xml --cov-report=term-missing || true
        continue-on-error: true

      # JavaScript Tests (skip if not needed)
      - name: Run JavaScript tests with coverage
        run: |
          npm test -- --coverage --watchAll=false || true
        continue-on-error: true

      # Copy Coverage Files (adjust for your setup)
      - name: Copy coverage files for SonarQube
        run: |
          # Copy Jest coverage if it exists
          if [ -f "coverage/lcov.info" ]; then
            cp coverage/lcov.info lcov.info
            echo "✅ Copied coverage/lcov.info to lcov.info"
          fi
          # Verify coverage files exist
          ls -la coverage.xml lcov.info 2>/dev/null || echo "⚠️ Coverage files not found"

      # SonarQube Scan
      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@v5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}

      # Quality Gate Check
      - name: SonarQube Quality Gate Check
        uses: SonarSource/sonarqube-quality-gate-action@v1
        timeout-minutes: 5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        continue-on-error: false  # Fail PR if quality gate fails
```

**Customization:**
- Remove language-specific steps you don't need (Python or Node.js)
- Adjust Python/Node versions
- Update test commands for your framework
- Modify coverage file copy logic
- Change timeout-minutes if scans take longer

---

## Phase 4: SonarQube Project Setup

### Step 4.1: Add GitHub Secrets

1. Go to: `https://github.com/YOUR-ORG/YOUR-REPO/settings/secrets/actions`
2. Click "New repository secret"
3. Add `SONAR_TOKEN`:
   - Name: `SONAR_TOKEN`
   - Value: Your SonarQube authentication token
4. Add `SONAR_HOST_URL`:
   - Name: `SONAR_HOST_URL`
   - Value: Your SonarQube instance URL (e.g., `http://your-sonarqube.com:9000`)

### Step 4.2: Create SonarQube Project

1. Log into your SonarQube instance
2. Click "Create Project" → "Manually"
3. Enter Project Key (must match `sonar-project.properties`)
4. Choose "GitHub Actions" as analysis method
5. Follow on-screen instructions

### Step 4.3: Configure Quality Gates

1. In SonarQube, go to Project Settings → Quality Gates
2. Select or create quality gate with thresholds:
   - Coverage on New Code: 80%+
   - Duplicated Lines: <3%
   - Maintainability Rating: A
   - Reliability Rating: A
   - Security Rating: A

---

## Phase 5: Validation

### Step 5.1: Create Test PR

```bash
# Create a new branch
git checkout -b feature/sonarqube-integration

# Add all configuration files
git add sonar-project.properties .gitignore README.md \
  .github/workflows/sonarqube.yml pytest.ini jest.config.js \
  package.json requirements.txt

# Commit changes
git commit -m "Add SonarQube integration"

# Push and create PR
git push -u origin feature/sonarqube-integration
gh pr create --title "Add SonarQube integration" --body "Set up automated code quality monitoring"
```

### Step 5.2: Verify Workflow

1. Watch GitHub Actions run
2. Check "SonarQube Scan" status check appears
3. Verify quality gate passes
4. Confirm badges appear in README (may take first scan)

### Step 5.3: Check SonarQube Dashboard

Visit: `http://YOUR-SONARQUBE-URL/dashboard?id=YOUR-PROJECT-KEY`

Verify:
- Project appears
- Code is analyzed
- Coverage data shows (if tests exist)
- Metrics populate

---

## Customization

### Multi-Module Projects

For projects with multiple modules:

```properties
sonar.sources=module1/src,module2/src,module3/src
sonar.tests=module1/tests,module2/tests,module3/tests
```

### Monorepos

Create separate `sonar-project.properties` in each subproject or use modules:

```properties
sonar.modules=frontend,backend
frontend.sonar.projectName=My App - Frontend
frontend.sonar.sources=frontend/src
backend.sonar.projectName=My App - Backend
backend.sonar.sources=backend/src
```

### Different Languages

#### Java
```properties
sonar.java.binaries=target/classes
sonar.java.source=11
sonar.junit.reportPaths=target/surefire-reports
```

#### Go
```properties
sonar.go.coverage.reportPaths=coverage.out
sonar.test.inclusions=**/*_test.go
```

#### PHP
```properties
sonar.php.coverage.reportPaths=coverage.xml
sonar.php.tests.reportPath=phpunit.xml
```

### Custom Quality Profiles

1. In SonarQube, go to Quality Profiles
2. Create custom profile or extend default
3. Assign to your project in Project Settings

---

## Troubleshooting

### Scan Fails with Authentication Error

**Check:**
- `SONAR_TOKEN` secret exists and is valid
- `SONAR_HOST_URL` is correct
- Token has "Execute Analysis" permission

**Fix:**
```bash
# Verify secrets exist
gh secret list

# Regenerate token in SonarQube if needed
# Update GitHub secret with new token
```

### Coverage Not Showing

**Check:**
- Coverage files are generated (`coverage.xml`, `lcov.info`)
- File paths match `sonar-project.properties`
- Coverage files are copied to project root

**Debug:**
```bash
# Run tests locally
pytest --cov=app --cov-report=xml
npm test -- --coverage

# Verify files exist
ls -la coverage.xml coverage/lcov.info
```

### Quality Gate Fails

**Common causes:**
- Low coverage on new code
- New bugs or vulnerabilities introduced
- Code duplications
- Too many code smells

**Fix:**
- Add tests to increase coverage
- Fix identified issues
- Refactor duplicate code
- Clean up code smells

### Badges Not Displaying

**Check:**
- First scan has completed
- Badge URLs use correct SonarQube URL and project key
- SonarQube instance is accessible publicly (if needed)

**Test:**
```bash
curl -I "http://YOUR-SONARQUBE-URL/api/project_badges/measure?project=YOUR-PROJECT-KEY&metric=alert_status"
# Should return 200 OK
```

### Workflow Times Out

**Solutions:**
- Increase `timeout-minutes` in quality gate step
- Optimize test execution
- Add more exclusions to reduce analysis scope
- Check SonarQube server performance

---

## Best Practices

### 1. Start Permissive

Begin with lenient quality gates and gradually tighten:
- Initial coverage: 60%
- After baseline established: 70%
- For new projects: 80%+

### 2. Use Branch Analysis

Configure SonarQube to analyze all branches:
```yaml
on:
  push:
    branches: ['**']  # All branches
  pull_request:
    branches: [main]
```

### 3. Separate Coverage from Scan

Use `continue-on-error: true` for test steps so scan runs even if tests fail.

### 4. Monitor Technical Debt

Set up SonarQube notifications for:
- Quality gate failures
- New critical issues
- Coverage drops

### 5. Regular Maintenance

- Review and fix security hotspots monthly
- Update quality gates quarterly
- Clean up false positives
- Update SonarQube and plugins

---

## Complete Example

For a full working example, see:
- **Repository:** https://github.com/adamkwhite/baseball-lineup-app
- **PR:** https://github.com/adamkwhite/baseball-lineup-app/pull/28
- **SonarQube Dashboard:** <YOUR_SONARQUBE_URL>/dashboard?id=baseball-lineup-app

---

## Resources

- **SonarQube Documentation:** https://docs.sonarqube.org/
- **GitHub Actions Docs:** https://docs.github.com/en/actions
- **SonarQube Scan Action:** https://github.com/SonarSource/sonarqube-scan-action
- **Quality Gate Action:** https://github.com/SonarSource/sonarqube-quality-gate-action

---

**Version:** 1.0
**Last Updated:** 2025-09-29
**Tested With:** SonarQube Community Edition, GitHub Actions