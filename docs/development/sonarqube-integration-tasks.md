## Relevant Files

- `sonar-project.properties` - SonarQube project configuration (✅ created)
- `.gitignore` - Git ignore patterns including .scannerwork/ (✅ updated)
- `README.md` - Project documentation with SonarQube badges (✅ updated with badges, needs URL update)
- `.github/workflows/sonarqube.yml` - GitHub Actions workflow for SonarQube scanning
- `pytest.ini` - pytest configuration for coverage reporting
- `jest.config.js` - Jest configuration for JavaScript coverage reporting
- `requirements.txt` - Python dependencies including pytest-cov

### Notes

- Phase 1 basic configuration is partially complete (sonar-project.properties, .gitignore, README badges added)
- Badge URLs in README.md need to be updated with actual SonarQube instance domain
- Testing infrastructure setup is tracked in separate feature: docs/features/comprehensive-testing-PLANNED/
- SonarQube analysis requires test coverage reports to be generated first

## Tasks

- [x] 1.0 Complete Basic Configuration Setup
  - [x] 1.1 Create sonar-project.properties with baseball-lineup-app, Python 3.12, and appropriate exclusions
  - [x] 1.2 Add .scannerwork/ directory to .gitignore
  - [x] 1.3 Add 11 comprehensive SonarQube badges to README.md (Quality Gate, Coverage, Bugs, Vulnerabilities, Code Smells, Security Rating, Maintainability Rating, Reliability Rating, Lines of Code, Duplicated Lines, Technical Debt)
  - [x] 1.4 Update README.md badge URLs from placeholder 'sonarqube.yourdomain.com' to actual SonarQube instance URL (http://44.206.255.230:9000)
  - [x] 1.5 Verify sonar-project.properties exclusions match project structure and add certificate/image file exclusions

- [ ] 2.0 Set Up Test Coverage Reporting Infrastructure
  - [ ] 2.1 Add pytest-cov to requirements.txt if not already present
  - [ ] 2.2 Create or update pytest.ini with coverage settings (--cov-report=xml, --cov-report=html, 80%+ threshold)
  - [ ] 2.3 Configure pytest to output coverage.xml in project root for SonarQube ingestion
  - [ ] 2.4 Create or update jest.config.js with coverage settings for JavaScript (lcov and xml formats, 85%+ threshold)
  - [ ] 2.5 Configure Jest to output coverage reports compatible with SonarQube
  - [ ] 2.6 Test local coverage report generation for both Python and JavaScript components

- [ ] 3.0 Create GitHub Actions Workflow for SonarQube Scanning
  - [ ] 3.1 Create .github/workflows/sonarqube.yml workflow file
  - [ ] 3.2 Configure workflow triggers (push to main, pull_request events)
  - [ ] 3.3 Add Python 3.12 setup step in workflow
  - [ ] 3.4 Add Node.js setup step for JavaScript analysis
  - [ ] 3.5 Add step to install Python dependencies and run pytest with coverage
  - [ ] 3.6 Add step to install Node dependencies and run Jest with coverage (if applicable)
  - [ ] 3.7 Add SonarSource/sonarqube-scan-action@v5 step with SONAR_TOKEN and SONAR_HOST_URL
  - [ ] 3.8 Add sonarqube-quality-gate-action step to enforce quality gate checks
  - [ ] 3.9 Configure workflow to fail PR if quality gate fails

- [ ] 4.0 Configure SonarQube Project and Quality Gates
  - [ ] 4.1 Verify SONAR_TOKEN and SONAR_HOST_URL secrets exist in GitHub repository settings
  - [ ] 4.2 Create baseball-lineup-app project in SonarQube Community instance
  - [ ] 4.3 Configure quality gate thresholds matching claude-memory-mcp standards
  - [ ] 4.4 Set coverage threshold for new code (80%+ for Python, 85%+ for JavaScript)
  - [ ] 4.5 Enable security vulnerability detection and configure security hotspot review
  - [ ] 4.6 Run initial SonarQube scan locally or via GitHub Actions to verify setup

- [ ] 5.0 Validate Integration and Update Documentation
  - [ ] 5.1 Trigger GitHub Actions workflow and verify SonarQube scan completes successfully
  - [ ] 5.2 Verify coverage reports appear in SonarQube dashboard
  - [ ] 5.3 Verify quality gate status is visible in GitHub PR checks
  - [ ] 5.4 Verify all 11 badges in README.md display correctly with live data
  - [ ] 5.5 Document SonarQube integration in development workflow documentation
  - [ ] 5.6 Create troubleshooting guide for common SonarQube scan issues
  - [ ] 5.7 Update PRD acceptance criteria to mark all items as complete