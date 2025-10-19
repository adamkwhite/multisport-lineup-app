# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Type**: Web application for youth sports team management
**Purpose**: Generates optimized lineups for multiple sports (baseball, soccer, volleyball) with TeamSnap integration
**Status**: MVP complete for baseball, multi-sport support in active development
**Current Branch**: main

## Tech Stack

- **Backend**: Python 3.x, Flask
- **Frontend**: HTML/CSS/JavaScript
- **Database**: SQLite (development), PostgreSQL (production)
- **API Integration**: TeamSnap API (OAuth 2.0)
- **Testing**: pytest, pytest-cov (94%+ coverage target)
- **CI/CD**: GitHub Actions (3-stage pipeline), SonarCloud
- **Code Quality**: Black, isort, flake8, mypy, bandit
- **Security**: gitleaks (secret scanning), pre-commit hooks

## Key Features

### Implemented
- TeamSnap OAuth integration for team/player data import
- Baseball lineup generation with pitcher rotation
- Visual baseball diamond field graphics
- Print-friendly layouts for field use
- Position preferences and smart assignment algorithm
- SSL/HTTPS support for OAuth callbacks
- Sport configuration system (JSON-based: baseball, soccer, volleyball)

### In Development
- Soccer lineup generation with goalkeeper requirements (Issue #53 remaining)

## Development Setup

### Prerequisites
- Python 3.x, pip
- TeamSnap API credentials (from TeamSnap Developer Portal)

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env and add TeamSnap credentials
cp .env.example .env
echo "FLASK_SSL=true" >> .env

# Start application (HTTPS required for TeamSnap OAuth)
./start.sh
```

**Access**: https://localhost:5000 (accept self-signed cert warning)

### Key Commands
```bash
./start.sh                           # Start app with SSL (preferred)
FLASK_SSL=true python3 app.py        # Manual startup

# Testing
./lineup-venv/bin/pytest tests/unit/ tests/edge_cases/ -v
./lineup-venv/bin/pytest --cov=app --cov=sports --cov-report=term-missing

# Pre-commit hooks
pre-commit run --all-files           # Run all checks
pre-commit install                   # One-time setup
```

## CI/CD Pipeline

**3-Stage GitHub Actions Workflow** (`.github/workflows/pr-validation.yml`):
1. **Quick Validation** (15-30s) - Code formatting, import sorting, linting
2. **Tests & SonarCloud** (2-3min) - Unit tests, coverage, quality gate
3. **Claude Review** (3-5min) - AI-powered code review

**Key Features:**
- 6 layers of safeguards ensure test failures block pipeline
- SonarCloud integration (public dashboard: https://sonarcloud.io/project/overview?id=adamkwhite_multisport-lineup-app)
- See `docs/development/ci-cd-pipeline.md` for full documentation

## Project Structure

```
multisport-lineup-app/
├── ai_docs/               # AI-specific documentation (PRD workflow)
├── config/sports/         # Sport-specific JSON configs
├── docs/                  # Documentation (deployment, development, features, testing)
├── scripts/               # Build and deployment scripts
├── sports/                # Multi-sport support (generators, models, services)
├── static/                # CSS, JS, images
├── templates/             # HTML templates
├── tests/                 # Test suite (api, edge_cases, fixtures, unit, visual)
├── app.py                 # Main Flask application
└── start.sh               # Startup script
```

See directory tree for complete structure.

## API Integration

### TeamSnap API
- **Authentication**: OAuth 2.0 required
- **HTTPS Requirement**: Mandatory for redirect URIs
- **Environment Variables**: See `.env.example`
  - `TEAMSNAP_CLIENT_ID`
  - `TEAMSNAP_CLIENT_SECRET`
  - `TEAMSNAP_REDIRECT_URI`

### Application Endpoints
- `/` - Home page
- `/auth/teamsnap` - OAuth initialization
- `/auth/callback` - OAuth callback handler
- `/teams` - List imported teams
- `/generate-lineup` - Create lineup for selected team
- `/print-lineup` - Print-friendly lineup view

## Dependencies

### External Services
- **TeamSnap API**: OAuth 2.0 authentication, team/player data import (requires credentials from TeamSnap Developer Portal)
- **SonarCloud**: Code quality analysis (public dashboard, "Sonar way" quality gate: 80%+ coverage, 0 bugs/vulnerabilities)

### Development Tools
- **Pre-commit hooks**: Black, isort, Flake8, gitleaks (v8.18.4)
- **CI/CD**: Black, isort, flake8, mypy, bandit
- **Playwright**: Visual regression tests
- See `requirements.txt` for Python packages

## Deployment

See `docs/deployment/` for detailed deployment guides.

**Quick Reference:**
- Heroku deployment instructions: `docs/deployment/heroku.md`
- Production considerations: PostgreSQL, SSL/TLS certificates, multi-user auth, rate limiting

## Known Issues

- **Virtual environment required**: Ubuntu 24.04+ requires venv for pip installs
- **Port conflicts**: Check port 5000 availability before starting
- **Self-signed certificates**: Browser warnings expected in local development
- **TeamSnap API rate limiting**: Not yet implemented for production

## Git Workflow (MANDATORY)

### 🚨 CRITICAL: Branch Workflow
- **NEVER commit directly to main branch**
- **ALWAYS create a feature branch first** - NO EXCEPTIONS
- Even for small fixes, typos, or documentation - use branches and PRs

**Process:**
1. Create branch: `git checkout -b feature/description` or `fix/bug-name`
2. Make changes and commit
3. Push branch: `git push -u origin branch-name`
4. Create PR: `gh pr create`
5. Wait for CI/CD checks to pass
6. **Ask user before merging** - Never merge without approval

**Branch naming:**
- `feature/description` - New features
- `fix/bug-name` - Bug fixes
- `docs/topic` - Documentation updates

See global `~/Code/CLAUDE.md` for complete Git workflow documentation.

## Important Notes

- **HTTPS Required**: TeamSnap OAuth requires HTTPS for redirect URIs
- **Self-Signed Certificates**: Local development uses self-signed certificates (browser warnings expected)
- **Print Optimization**: Designs optimized for printing on field (landscape layouts, clear fonts)
- **PRD Workflow**: Use `ai_docs/create-prd.mdc` for creating new feature PRDs with GitHub issue tracking
- **Test Coverage**: Maintain 94%+ coverage (currently 353 tests passing)

## Recent Changes

**2025-10-19 (Session 8)**: SonarCloud MCP integration and documentation optimization
- Successfully integrated SonarCloud MCP server (Docker-based, now operational)
- Optimized CLAUDE.md: 479→224 lines (53% reduction, ~3k tokens saved)
- Created `docs/archive/CHANGELOG.md` for detailed session history
- Updated `/StartOfTheDay` and `/WrapUpForTheDay` slash commands for new workflow

**2025-10-18 (Session 7)**: Security hardening and pre-commit infrastructure
- Added gitleaks v8.18.4 secret scanning to pre-commit hooks (PR #91)
- Comprehensive pre-commit hooks documentation (PR #90)
- Fixed OAuth sport context preservation (PR #89)
- Maintained 94%+ test coverage, all quality gates passed

For detailed session history, see `docs/archive/CHANGELOG.md`

## Current Architecture

- **Factory pattern**: Runtime sport selection via `get_lineup_generator(sport_id)` (Issue #50 ✅)
- **Sport-specific generators**:
  - `BaseballLineupGenerator` with pitcher rotation (Issue #49 ✅)
  - `VolleyballLineupGenerator` with rotation tracking (Issue #51 ✅)
- **Abstract base class**: `LineupGenerator` with shared data models (Issue #48 ✅)
- **Sport configuration**: JSON-based configs loaded via `sport_loader.py` (Issue #39 ✅)
- **Smart position assignment**: Algorithm with history tracking
- **API endpoint**: Sport-agnostic `/api/lineup/generate` with 400/501 error handling

## Next Steps

**Immediate:**
- Complete sport-specific configuration rules (Issue #53)

**Short-term:**
- Update frontend UI for multi-sport selection
- Add sport selector to lineup generation form
- Update visual field diagrams for soccer/volleyball

**Medium-term:**
- Multi-user/multi-tenant architecture
- Payment integration (subscription-based)
- Advanced lineup optimization algorithms
- Season-long statistics tracking
