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
- Sport-specific lineup generators (Issues #48-#53)
- Abstract LineupGenerator base class
- Soccer lineup generation with goalkeeper requirements
- Volleyball lineup generation with rotation

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
baseball-lineup-app/
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
heroku create baseball-lineup-app

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
- Black, isort, flake8, mypy, bandit (configured via pre-commit hooks)
- Playwright (visual regression tests)

## Known Issues

- **Virtual environment required**: Ubuntu 24.04+ requires venv for pip installs
- **Port conflicts**: Check port 5000 availability before starting app
- **Self-signed certificates**: Browser warnings expected in local development
- **TeamSnap API rate limiting**: Not yet implemented for production use

## Important Notes

- **HTTPS Required**: TeamSnap OAuth requires HTTPS for redirect URIs
- **Self-Signed Certificates**: Local development uses self-signed certificates (browser warnings expected)
- **TeamSnap API**: Requires approved application and API credentials from TeamSnap Developer Portal
- **Print Optimization**: Designs optimized for printing on field (landscape layouts, clear fonts)
- **PRD Workflow**: Use `ai_docs/create-prd.mdc` for creating new feature PRDs with GitHub issue tracking

## Recent Changes

**2025-10-06**: Multi-sport lineup generator planning
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
- **Monolithic lineup generation**: All baseball logic in `app.py` (~400 lines)
- **Sport configuration**: JSON-based configs loaded via `sport_loader.py`
- **Smart position assignment**: `assign_positions_smart()` with history tracking
- **Pitcher rotation**: Max 2 consecutive innings enforced

### Planned Architecture (In Progress)
- **Abstract base class**: `LineupGenerator` with sport-specific implementations
- **Factory pattern**: Runtime sport selection via `get_lineup_generator(sport_id)`
- **Shared utilities**: Common functions in `sports/utils/lineup_utils.py`
- **Sport-specific rules**: Configurable via JSON (pitcher max innings, goalkeeper requirements, etc.)

## Next Steps

**Immediate** (Issue #48):
- Create `LineupGenerator` abstract base class
- Implement shared data models (Player, Lineup, PositionAssignment)
- Build common utility functions (assign_positions_smart, history tracking)
- 35+ unit tests with 95%+ coverage

**Short-term** (Issues #49-#53):
- Extract baseball logic into `BaseballLineupGenerator`
- Implement `SoccerLineupGenerator` with goalkeeper rules
- Implement `VolleyballLineupGenerator` with rotation
- Create factory for runtime sport selection
- Add sport-specific configuration rules

**Medium-term**:
- Integrate generators into app.py
- Update UI for multi-sport selection
- End-to-end testing for all 3 sports

## Roadmap

### Completed
- ✅ TeamSnap OAuth integration
- ✅ Baseball lineup generation with pitcher rotation
- ✅ Visual baseball diamond graphics
- ✅ Print-friendly layouts
- ✅ Position preference handling
- ✅ Sport configuration backend (Issue #39)
- ✅ CI/CD pipeline with SonarQube

### In Progress
- 🔄 Multi-sport lineup generators (Issues #48-#53)

### Planned
- 🔲 Multi-user/multi-tenant architecture
- 🔲 Payment integration (subscription-based)
- 🔲 Advanced lineup optimization algorithms
- 🔲 Season-long statistics tracking
- 🔲 Mobile-responsive design improvements
- 🔲 Additional sports support (softball, T-ball)
