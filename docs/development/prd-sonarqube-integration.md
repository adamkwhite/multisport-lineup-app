# PRD: SonarQube Integration for Baseball Lineup App

## Overview

Integrate the Baseball Lineup App project with SonarQube for continuous code quality monitoring, following the same configuration patterns as the existing claude-memory-mcp project.

## Problem Statement

The Baseball Lineup App project currently lacks automated code quality monitoring and analysis. To maintain consistency with other projects and ensure high code quality standards, we need to integrate this project with the existing SonarQube instance.

## Goals

### Primary Goals
- **Code Quality Monitoring**: Implement continuous code quality analysis for Python (98.7%) and JavaScript (0.1%) codebase
- **CI/CD Integration**: Automate SonarQube scanning in GitHub Actions workflow
- **Quality Gates**: Enforce quality standards before code merges
- **Coverage Tracking**: Monitor test coverage and maintain quality thresholds

### Secondary Goals
- **Consistency**: Match configuration patterns from claude-memory-mcp project
- **Security Analysis**: Detect potential security vulnerabilities in code
- **Technical Debt**: Track and monitor technical debt accumulation
- **Visual Quality Dashboard**: Display comprehensive quality metrics in README with SonarQube badges

## Success Criteria

- [ ] SonarQube project successfully created and configured
- [ ] GitHub Actions workflow runs SonarQube analysis on every PR/push
- [ ] Quality gate passes with acceptable thresholds
- [ ] Test coverage reports are properly integrated
- [ ] Code smells and security hotspots are identified and tracked

## Requirements

### Functional Requirements

1. **Project Configuration**
   - Create sonar-project.properties with appropriate settings
   - Configure Python version (3.12) and source paths
   - Set appropriate exclusions for generated files, test artifacts, virtual environments, and documentation
   - Add comprehensive README badges matching claude-memory-mcp format (11 badges total)

2. **CI/CD Integration**
   - Integrate SonarQube scanning into existing GitHub Actions workflow
   - Configure quality gate checks to prevent merging failing code
   - Generate and upload test coverage reports

3. **Quality Standards**
   - Match quality gate settings from claude-memory-mcp project
   - Configure appropriate thresholds for coverage, duplications, and maintainability
   - Enable security vulnerability detection

### Technical Requirements

1. **Environment Configuration**
   - Use existing SonarQube Community instance
   - Leverage existing SONAR_TOKEN and SONAR_HOST_URL secrets
   - Support Python 3.12 analysis
   - Support JavaScript analysis for frontend components

2. **Test Integration**
   - Configure pytest for backend Python coverage reporting (targeting 80%+ coverage)
   - Configure Jest for frontend JavaScript coverage reporting (targeting 85%+ coverage)
   - Generate XML coverage reports compatible with SonarQube
   - Exclude test files from coverage analysis where appropriate

3. **Project Structure Compatibility**
   - Work with root-level app.py structure (not src/ directory)
   - Handle Flask application patterns
   - Exclude virtual environment (lineup-venv/), test results, and coverage directories
   - Exclude documentation (docs/), development tasks (ai-dev-tasks/), and scripts
   - Exclude node_modules and frontend build artifacts

### Non-Functional Requirements

1. **Performance**
   - SonarQube analysis should complete within 5 minutes
   - Minimal impact on existing CI/CD pipeline performance

2. **Security**
   - No exposure of sensitive configuration data
   - Secure token handling in GitHub Actions

3. **Maintainability**
   - Configuration should be easily updateable
   - Clear documentation for quality thresholds

## User Stories

### As a Developer
- I want automated code quality checks on every PR so I can catch issues early
- I want to see test coverage reports so I can identify untested code
- I want security vulnerability alerts so I can address potential risks

### As a Project Maintainer
- I want quality gates to prevent low-quality code from being merged
- I want consistent quality standards across all MCP projects
- I want visibility into technical debt trends over time

## Technical Specifications

### SonarQube Configuration
```properties
sonar.projectKey=multisport-lineup-app
sonar.python.version=3.12
sonar.python.coverage.reportPaths=coverage.xml
sonar.sources=.
sonar.exclusions=**/*test*/**,**/__pycache__/**,lineup-venv/**,venv/**,htmlcov/**,test-results/**,scripts/**,docs/**,ai-dev-tasks/**,node_modules/**
```

### README Badge Configuration
Add comprehensive SonarQube badges to README.md following claude-memory-mcp pattern:
- Quality Gate Status
- Coverage
- Bugs
- Vulnerabilities
- Code Smells
- Security Rating
- Maintainability Rating
- Reliability Rating
- Lines of Code
- Duplicated Lines (%)
- Technical Debt

### GitHub Actions Integration
- Integrate with existing workflow or create new build.yml
- Use SonarSource/sonarqube-scan-action@v5
- Include quality gate check with timeout
- Generate coverage reports before SonarQube scan

### Test Coverage Setup
- Configure pytest-cov for Python/Flask backend XML coverage output (80%+ target)
- Configure Jest for JavaScript frontend XML coverage output (85%+ target)
- Set up test infrastructure following testing-infrastructure-template.mdc
- Exclude test files, virtual environments, and configuration from coverage metrics
- Generate timestamped test results in test-results/ directory

## Dependencies

### External Dependencies
- Existing SonarQube instance (already configured)
- GitHub repository secrets (SONAR_TOKEN, SONAR_HOST_URL)
- pytest and pytest-cov packages

### Internal Dependencies
- Current project structure (root-level app.py, templates/, static/)
- Planned testing framework from comprehensive-testing-PLANNED feature
- GitHub Actions workflow capability
- Flask application backend
- JavaScript frontend components

## Timeline

### Phase 1: Basic Integration (Day 1) ✅
- ✅ Create sonar-project.properties with multisport-lineup-app configuration
- ✅ Add .scannerwork/ to .gitignore
- ✅ Add comprehensive SonarQube badges to README.md (11 badges)
- ⏳ Set up GitHub Actions workflow
- ⏳ Configure project in SonarQube instance

### Phase 2: Quality Gates (Day 1)
- Configure quality gate thresholds
- Add coverage reporting
- Test full pipeline

### Phase 3: Optimization (Day 2)
- Fine-tune exclusions and settings
- Optimize performance
- Document configuration

## Risks and Mitigation

### Risk: SonarQube Analysis Failures
- **Mitigation**: Start with permissive settings, gradually tighten
- **Fallback**: Allow manual override for urgent fixes

### Risk: Coverage Reporting Issues
- **Mitigation**: Test coverage generation locally first
- **Fallback**: Start without coverage requirements, add incrementally

### Risk: Pipeline Performance Impact
- **Mitigation**: Monitor build times and optimize if needed
- **Fallback**: Run SonarQube on main branch only if too slow

## Out of Scope

- Custom SonarQube rules development
- Integration with other static analysis tools
- Historical code quality analysis migration
- Custom quality profiles (use default Python profile)

## Acceptance Criteria

1. **Configuration Complete**
   - ✅ sonar-project.properties created with correct settings (baseball-lineup-app, Python 3.12)
   - ✅ .gitignore updated with .scannerwork/
   - ✅ All exclusions properly configured (tests, venvs, docs, ai-dev-tasks, node_modules, test-results, htmlcov)
   - ⏳ Project appears in SonarQube dashboard

2. **CI/CD Integration Working**
   - GitHub Actions runs SonarQube scan successfully
   - Quality gate status visible in PR checks
   - Coverage reports uploaded and visible

3. **Quality Standards Met**
   - No blocking quality gate failures on main branch
   - Test coverage reporting functional
   - Security hotspots identified and reviewed

4. **Documentation Updated**
   - ✅ README updated with comprehensive SonarQube badge suite (11 badges)
   - ⏳ Badge URLs updated with actual SonarQube instance domain
   - ⏳ Development workflow documentation includes quality checks
   - ⏳ Troubleshooting guide for common issues
