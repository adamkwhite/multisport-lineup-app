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
- **Deployment**: Designed for Heroku
- **SSL/HTTPS**: Self-signed certificates for local development
- **Testing**: pytest, pytest-cov (94%+ coverage target)
- **CI/CD**: GitHub Actions (3-stage pipeline), SonarQube
- **Code Quality**: Black, isort, flake8, mypy, bandit

## Key Features

### Implemented
- TeamSnap OAuth integration for team/player data import
- Baseball lineup generation with pitcher rotation (2 innings max per pitcher)
- Visual baseball diamond field graphics
- Print-friendly layouts for field use
- Position preferences (pitcher, catcher, any position)
- Smart position assignment algorithm with player history tracking
- SSL/HTTPS support for OAuth callbacks
- Sport configuration system (JSON-based, supports baseball, soccer, volleyball)

### In Development
- Soccer lineup generation with goalkeeper requirements (Issue #53 remaining)

## Development Setup

### Prerequisites
```bash
# Python 3.x required
# pip package manager
# TeamSnap API credentials (from TeamSnap Developer Portal)
```

### Required Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env and add your TeamSnap API credentials
cp .env.example .env

# IMPORTANT: Add FLASK_SSL=true to .env file for HTTPS support
echo "FLASK_SSL=true" >> .env
```

### Startup Commands

**PREFERRED METHOD (handles SSL and environment automatically):**
```bash
./start.sh
```

**ALTERNATIVE MANUAL STARTUP:**
```bash
# For HTTPS (required for TeamSnap OAuth):
FLASK_SSL=true python3 app.py

# For HTTP only (development testing):
python3 app.py
```

**Access**: https://localhost:5000 (HTTPS required for TeamSnap OAuth)
**Note**: Accept security warning for self-signed certificate in browser

## Development Commands

```bash
# Start application with SSL
./start.sh

# Start application manually with HTTPS
FLASK_SSL=true python3 app.py

# Start application without SSL (limited functionality)
python3 app.py

# Install new dependencies
pip install <package-name>
pip freeze > requirements.txt

# Pre-commit hooks (run automatically on commit)
pre-commit run --all-files  # Run all checks manually
pre-commit run black        # Run specific check
pre-commit install          # Install git hooks (one-time setup)

# Database operations (if applicable)
python3 manage.py db migrate
python3 manage.py db upgrade
```

## CI/CD Pipeline

**3-Stage GitHub Actions Workflow** (`.github/workflows/pr-validation.yml`):

1. **Quick Validation** (15-30s) - Code formatting, import sorting, linting
2. **Tests & SonarQube** (2-3min) - Unit tests, coverage, quality gate
3. **Claude Review** (3-5min) - AI-powered code review

**Key Features:**
- 6 layers of safeguards ensure test failures block pipeline
- SonarQube integration for code quality tracking
- isort configured with Black profile (`.isort.cfg`)
- See `docs/development/ci-cd-pipeline.md` for full documentation

## Testing

```bash
# Run unit and edge case tests
./lineup-venv/bin/pytest tests/unit/ tests/edge_cases/ -v

# Run with coverage
./lineup-venv/bin/pytest tests/unit/ tests/edge_cases/ --cov=app --cov-report=term-missing

# Run specific test file
./lineup-venv/bin/pytest tests/unit/test_lineup_generation.py -v

# Run visual regression tests (requires app running)
./lineup-venv/bin/pytest tests/visual/ -v
```

**Test Coverage:** 94%+ (151/153 tests passing)
**Test Organization:** Unit, edge cases, visual regression
**Documentation:** `docs/testing/guidelines.md`

## API Integration

### TeamSnap API
- **Authentication**: OAuth 2.0 required
- **HTTPS Requirement**: Mandatory for redirect URIs
- **Rate Limiting**: Considerations for production deployment
- **Response Format**: Collection+JSON format for API responses
- **Environment Variables**: See `.env.example` for required credentials
  - `TEAMSNAP_CLIENT_ID`
  - `TEAMSNAP_CLIENT_SECRET`
  - `TEAMSNAP_REDIRECT_URI`

### API Endpoints (Application)
- `/` - Home page
- `/auth/teamsnap` - TeamSnap OAuth initialization
- `/auth/callback` - OAuth callback handler
- `/teams` - List imported teams
- `/generate-lineup` - Create lineup for selected team
- `/print-lineup` - Print-friendly lineup view

## Project Structure

```
multisport-lineup-app/
├── ai_docs/               # AI-specific documentation (PRD workflow, etc.)
├── config/                # Configuration files
│   └── sports/            # Sport-specific JSON configs (baseball, soccer, volleyball)
├── docs/                  # Documentation and design materials
│   ├── archive/           # Archived documentation
│   ├── deployment/        # Deployment guides
│   ├── development/       # Development documentation (CI/CD, etc.)
│   ├── features/          # Feature PRDs and planning
│   ├── screenshots/       # UI reference files
│   └── testing/           # Testing documentation
├── scripts/               # Build and deployment scripts
├── sports/                # Multi-sport support modules
│   ├── generators/        # Lineup generators (planned: base, baseball, soccer, volleyball)
│   ├── models/            # Sport data models (SportConfig, Position, etc.)
│   ├── services/          # Sport services (sport_loader)
│   └── utils/             # Shared utilities (planned)
├── static/                # CSS, JS, images
├── templates/             # HTML templates
├── tests/                 # Test suite
│   ├── api/               # API integration tests
│   ├── edge_cases/        # Edge case tests
│   ├── fixtures/          # Test fixtures
│   ├── unit/              # Unit tests
│   └── visual/            # Visual regression tests
├── .env.example           # Environment template
├── app.py                 # Main Flask application
├── CLAUDE.md              # Project context for Claude AI
├── README.md              # Project overview
├── requirements.txt       # Python dependencies
└── start.sh               # Startup script (symlink to scripts/start.sh)
```

## Deployment

### Heroku Deployment
```bash
# Login to Heroku
heroku login

# Create new app
heroku create multisport-lineup-app

# Set environment variables
heroku config:set TEAMSNAP_CLIENT_ID=your_client_id
heroku config:set TEAMSNAP_CLIENT_SECRET=your_client_secret
heroku config:set TEAMSNAP_REDIRECT_URI=https://your-app.herokuapp.com/auth/callback

# Deploy
git push heroku main

# Open application
heroku open
```

### Production Considerations
- PostgreSQL database instead of SQLite
- Environment-based configuration
- SSL/TLS certificates from trusted CA
- TeamSnap API rate limiting handling
- Multi-user authentication system
- Payment integration (planned)

## Dependencies

### External Services
- **TeamSnap API**: OAuth 2.0 authentication, team/player data import
  - Requires client ID and secret from TeamSnap Developer Portal
  - HTTPS redirect URI mandatory
- **SonarQube**: Code quality analysis (production instance at 44.206.255.230:9000)

### Python Packages (requirements.txt)
- Flask, requests, pytest, pytest-cov
- See `requirements.txt` for complete list

### Development Tools
- **Pre-commit hooks**: Black, isort, Flake8 for local code quality checks
- **CI/CD Tools**: Black, isort, flake8, mypy, bandit (GitHub Actions)
- **Playwright**: Visual regression tests
- **Pre-commit package**: Installed in virtual environment (`pip install pre-commit`)

## Known Issues

- **Virtual environment required**: Ubuntu 24.04+ requires venv for pip installs
- **Port conflicts**: Check port 5000 availability before starting app
- **Self-signed certificates**: Browser warnings expected in local development
- **TeamSnap API rate limiting**: Not yet implemented for production use

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
- **TeamSnap API**: Requires approved application and API credentials from TeamSnap Developer Portal
- **Print Optimization**: Designs optimized for printing on field (landscape layouts, clear fonts)
- **PRD Workflow**: Use `ai_docs/create-prd.mdc` for creating new feature PRDs with GitHub issue tracking

## Recent Changes

**2025-10-07 (Session 5)**: Infrastructure improvements and workflow enforcement
- **Fixed demo mode bug** (commit 41e6827 - direct to main, later corrected)
  - Changed position checkbox values from numeric to position IDs ('P', 'C', '1B' vs 1, 2, 3)
  - Fixed "Cannot convert undefined or null to object" error in lineup generation
  - Updated `generateLineup()` JS to use string values instead of parseInt()
- **Completed Issue #53**: Sport-specific generation rules configuration (PR #64)
  - Added `generation_rules` to all 3 sport configs (baseball, volleyball, soccer)
  - Updated `SportRules` dataclass with `generation_rules: Optional[Dict]` field
  - Generators now read rules from config instead of hardcoding (pitcher_max_innings, rotation_required, etc.)
  - Created 20 comprehensive tests in `tests/unit/test_generation_rules.py`
  - All 336 tests passing, 96%+ coverage maintained
- **Infrastructure PR #65**: CI coverage and code quality fixes
  - Added `sports/` module to CI coverage tracking (`--cov=app --cov=sports`)
  - Updated SonarQube to analyze sports/ directory
  - Fixed 6 code quality violations (type hints, unused params, cognitive complexity, etc.)
  - SonarQube quality gate: 95%+ coverage, 0 violations
- **Workflow enforcement** (PRs #67 and DevOps #1)
  - Added mandatory "🚨 CRITICAL: Branch Workflow" section to both CLAUDE.md files
  - Explicitly forbids direct commits to main - NO EXCEPTIONS
  - Updated global template in `~/Code/Devops/CLAUDE.md`
- **Created Issue #66**: Frontend multi-sport UI support (sport selection + field diagrams)
- **Closed Issue #63**: Already completed as part of Issue #53
- Multi-sport backend architecture complete ✅ (Issues #48, #49, #50, #51, #53 all closed)
- Next: Frontend UI for sport selection and sport-specific field diagrams

**2025-10-06 (Session 4)**: VolleyballLineupGenerator implementation (Issue #51)
- Implemented volleyball-specific lineup generation with basic rotation support
- Created `sports/generators/volleyball.py` with VolleyballLineupGenerator class
  - 6-position lineups (S, OH×2, MB×2, OPP/L/DS)
  - Variable sets (3-5 configurable via `num_sets` in game_info)
  - Position assignment with smart rotation via position history
  - Must-play logic for players benched 2+ consecutive sets
  - Bench tracking across sets
- Added 22 comprehensive unit tests (`tests/unit/test_volleyball_generator.py`)
- Updated factory pattern to support volleyball
  - Updated `get_lineup_generator()` to return VolleyballLineupGenerator
  - Updated `get_supported_sports()` to return `["baseball", "volleyball"]`
- All 316 tests passing ✅, coverage maintained
- Commit: `5b89f5e`, Issue #51 closed

**2025-10-06 (Session 3)**: Factory pattern implementation (Issue #50)
- Implemented factory pattern for sport-specific lineup generators
- Created `sports/services/lineup_factory.py` with runtime sport selection
  - `get_lineup_generator(sport_id)` - Main factory function
  - `get_supported_sports()` - Returns supported sports list
  - `is_sport_supported(sport_id)` - Validation helper
- Refactored `app.py` from 248 to 75 lines (70% reduction)
  - Replaced hard-coded baseball logic with factory pattern
  - Sport-agnostic `/api/lineup/generate` endpoint
  - Proper error handling (400, 501 status codes)
- Updated API response format (breaking change)
  - New: `assignments` list, `bench_players` list, `period` fields
  - Old: `lineup` dict, `bench` list, `pitcher` field
- Changed position IDs from integers to strings ("P", "C" vs 1, 2)
- Added 25 comprehensive factory tests
- Updated all test fixtures and integration tests
- All 293 tests passing, 96% coverage maintained
- Commit: `c541c22`, pushed to main

**2025-10-06 (Session 2)**: Pre-commit hooks and code quality improvements
- Added pre-commit hooks for local code quality checks (`.pre-commit-config.yaml`)
- Configured Black, isort, Flake8, and pre-commit-hooks for auto-fixing
- Fixed 8 SonarQube maintainability issues (PR #55)
  - Removed 7 unnecessary f-strings
  - Simplified duplicate branch logic
- Completed repository rebranding from baseball-lineup-app to multisport-lineup-app (PR #54)
  - Updated 30+ references across 15+ files
  - Cleaned up virtual environment from git history
  - Updated SonarQube project configuration
- Created DevOps template with pre-commit documentation (`~/Code/Devops/`)
- All 175 tests passing, 96% coverage maintained

**2025-10-06 (Session 1)**: Multi-sport lineup generator planning
- Created PRD for sport-specific lineup generators (`docs/features/sport-specific-lineup-generators-PLANNED/prd.md`)
- Created 6 GitHub issues (#48-#53) for implementation tracking
- Established cross-referencing between PRD and issues
- Renamed `ai-dev-tasks/` to `ai_docs/` for consistency

**2025-10-05**: Sport configuration system (Issue #39)
- Implemented JSON-based sport configuration system
- Created `sports/models/sport_config.py` with dataclasses
- Created `sports/services/sport_loader.py` with caching
- Added configurations for baseball, soccer, volleyball
- 27 comprehensive unit tests, 100% coverage

## Implementation Details

### Current Architecture
- **Factory pattern**: Runtime sport selection via `get_lineup_generator(sport_id)` (Issue #50 ✅)
- **Sport-specific generators**:
  - `BaseballLineupGenerator` with pitcher rotation (Issue #49 ✅)
  - `VolleyballLineupGenerator` with rotation tracking (Issue #51 ✅)
- **Abstract base class**: `LineupGenerator` with shared data models (Issue #48 ✅)
- **Sport configuration**: JSON-based configs loaded via `sport_loader.py` (Issue #39 ✅)
- **Smart position assignment**: Algorithm with history tracking
- **API endpoint**: Sport-agnostic `/api/lineup/generate` with 400/501 error handling

## Next Steps

**Immediate** (Issue #53):
- Add sport-specific configuration rules (Issue #53)
  - Pitcher max innings for baseball
  - Goalkeeper rotation rules for soccer
  - Set rotation patterns for volleyball

**Short-term**:
- Update frontend UI for multi-sport selection
- Add sport selector to lineup generation form
- Update visual field diagrams for soccer/volleyball

**Medium-term**:
- Multi-user/multi-tenant architecture
- Payment integration (subscription-based)
- Advanced lineup optimization algorithms
- Season-long statistics tracking

## Roadmap

### Completed
- ✅ TeamSnap OAuth integration
- ✅ Baseball lineup generation with pitcher rotation
- ✅ Visual baseball diamond graphics
- ✅ Print-friendly layouts
- ✅ Position preference handling
- ✅ Sport configuration backend (Issue #39)
- ✅ CI/CD pipeline with SonarQube
- ✅ Abstract LineupGenerator base class (Issue #48)
- ✅ BaseballLineupGenerator implementation (Issue #49)
- ✅ Factory pattern for runtime sport selection (Issue #50)
- ✅ VolleyballLineupGenerator with rotation support (Issue #51)

### In Progress
- 🔄 Sport-specific configuration rules (Issue #53)

### Planned
- 🔲 Multi-user/multi-tenant architecture
- 🔲 Payment integration (subscription-based)
- 🔲 Advanced lineup optimization algorithms
- 🔲 Season-long statistics tracking
- 🔲 Mobile-responsive design improvements
- 🔲 Additional sports support (softball, T-ball)
