# Baseball Lineup Manager

[![Quality Gate Status](http://44.206.255.230:9000/api/project_badges/measure?project=multisport-lineup-app&metric=alert_status)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Coverage](http://44.206.255.230:9000/api/project_badges/measure?project=multisport-lineup-app&metric=coverage)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Bugs](http://44.206.255.230:9000/api/project_badges/measure?project=multisport-lineup-app&metric=bugs)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Vulnerabilities](http://44.206.255.230:9000/api/project_badges/measure?project=multisport-lineup-app&metric=vulnerabilities)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Code Smells](http://44.206.255.230:9000/api/project_badges/measure?project=multisport-lineup-app&metric=code_smells)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Security Rating](http://44.206.255.230:9000/api/project_badges/measure?project=multisport-lineup-app&metric=security_rating)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Maintainability Rating](http://44.206.255.230:9000/api/project_badges/measure?project=multisport-lineup-app&metric=sqale_rating)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Reliability Rating](http://44.206.255.230:9000/api/project_badges/measure?project=multisport-lineup-app&metric=reliability_rating)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Lines of Code](http://44.206.255.230:9000/api/project_badges/measure?project=multisport-lineup-app&metric=ncloc)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Duplicated Lines (%)](http://44.206.255.230:9000/api/project_badges/measure?project=multisport-lineup-app&metric=duplicated_lines_density)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Technical Debt](http://44.206.255.230:9000/api/project_badges/measure?project=multisport-lineup-app&metric=sqale_index)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)

A web application that connects to the TeamSnap API to automatically generate baseball fielding positions for upcoming games.

## Features

- 🏟️ Fetch recent games from TeamSnap
- 👥 Get list of attending players
- ⚾ Generate optimal fielding positions
- 📱 Simple web interface for lineup management

## Setup

### Prerequisites
- Python 3.8+
- TeamSnap account and API credentials

### Installation

1. Clone and setup:
```bash
cd multisport-lineup-app
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your TeamSnap API credentials
```

3. Run locally:
```bash
python app.py
```

Visit `http://localhost:5000` to use the app.

## TeamSnap API Setup

1. Go to https://auth.teamsnap.com to register your application
2. Get your `client_id` and `client_secret`
3. Add them to your `.env` file

## Configuration

The app allows you to:
- Set preferred fielding positions for players
- Configure position rotation strategies
- Save and reuse lineup templates

## CI/CD Pipeline

The project uses a **3-stage GitHub Actions pipeline** for automated quality assurance:

1. **Quick Validation** (15-30s) - Black, isort, Flake8
2. **Tests & SonarQube** (2-3 min) - Unit tests, coverage, quality gate
3. **Claude Review** (3-5 min) - AI-powered code review

**Documentation:** See `docs/development/ci-cd-pipeline.md` for full details.

## Testing

The project has comprehensive test coverage (94%+):

### Run Unit and Edge Case Tests
```bash
./lineup-venv/bin/pytest tests/unit/ tests/edge_cases/ -v
```

### Run with Coverage Report
```bash
./lineup-venv/bin/pytest tests/unit/ tests/edge_cases/ --cov=app --cov-report=html --cov-report=term-missing
```

View HTML coverage report: `htmlcov/index.html`

### Run Visual Regression Tests
Visual tests require the Flask app to be running:
```bash
# Terminal 1: Start app
./start.sh

# Terminal 2: Run visual tests
./lineup-venv/bin/pytest tests/visual/ -v
```

**Note**: Visual tests are skipped by default. Remove `@pytest.mark.skip` decorator or run with `-m "not skip"`.

### Test Organization
- `tests/unit/` - Unit tests for core functionality
- `tests/edge_cases/` - Edge case and error handling tests
- `tests/visual/` - Playwright visual regression tests (20 tests)
- `tests/fixtures/` - Reusable test data and helpers
- `docs/testing/` - Comprehensive testing documentation

See `docs/testing/guidelines.md` for detailed testing documentation.

## Deployment

Can be deployed to:
- Heroku
- AWS EC2 (like your SBTM tool)
- Local development server