# SonarQube Integration - Usage Guide

## Overview

The Baseball Lineup App integrates with SonarQube for continuous code quality monitoring. SonarQube automatically scans code on every PR and push to main.

**SonarQube Dashboard:** <YOUR_SONARQUBE_URL>/dashboard?id=multisport-lineup-app

## Quality Metrics

11 key metrics tracked via README badges:
1. Quality Gate Status
2. Coverage
3. Bugs
4. Vulnerabilities
5. Code Smells
6. Security Rating
7. Maintainability Rating
8. Reliability Rating
9. Lines of Code
10. Duplicated Lines
11. Technical Debt

## Development Workflow

### Creating a PR
1. Push your branch to GitHub
2. Create a pull request to main
3. GitHub Actions automatically:
   - Runs Python tests with pytest
   - Runs JavaScript tests with Jest
   - Sends code to SonarQube
   - Checks quality gate
4. PR blocked if quality gate fails

### Quality Gate Thresholds
- Python Coverage: 80%+ for new code
- JavaScript Coverage: 85%+ for new code
- No security vulnerabilities
- Minimal code smells

## Running Tests Locally

### Python Tests
```bash
source lineup-venv/bin/activate
pytest tests/api/ --cov=app --cov-report=xml --cov-report=html
```

### JavaScript Tests
```bash
npm test -- --coverage
```

## Configuration

### sonar-project.properties
```properties
sonar.projectKey=multisport-lineup-app
sonar.python.version=3.12
sonar.python.coverage.reportPaths=coverage.xml
sonar.sources=.
sonar.exclusions=**/*test*/**,**/__pycache__/**,lineup-venv/**,venv/**,htmlcov/**,test-results/**,scripts/**,docs/**,ai-dev-tasks/**,node_modules/**,*.pem,*.png,*.jpg,*.jpeg,*.gif
```

### GitHub Secrets
- `SONAR_TOKEN` - SonarQube authentication token
- `SONAR_HOST_URL` - <YOUR_SONARQUBE_URL>

## Resources
- **Dashboard:** <YOUR_SONARQUBE_URL>/dashboard?id=multisport-lineup-app
- **Troubleshooting:** [sonarqube-troubleshooting.md](sonarqube-troubleshooting.md)