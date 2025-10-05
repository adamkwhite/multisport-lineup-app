# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Type**: Web application for youth baseball team management
**Purpose**: Generates optimized baseball lineups for 6-inning games with TeamSnap integration
**Status**: MVP complete, roadmap includes payment integration and multi-tenant architecture

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML/CSS/JavaScript
- **Database**: SQLite/PostgreSQL
- **API Integration**: TeamSnap API (OAuth 2.0)
- **Deployment**: Designed for Heroku
- **SSL/HTTPS**: Self-signed certificates for local development

## Key Features

- TeamSnap OAuth integration for team/player data import
- 3-lineup generation with pitcher rotation (2 innings max per pitcher)
- Visual baseball diamond field graphics
- Print-friendly layouts for field use
- Position preferences (pitcher, catcher, any position)
- Player randomization across lineups for development
- SSL/HTTPS support for OAuth callbacks

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

## Testing

```bash
# Run test suite (if implemented)
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_lineup_generation.py
```

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
├── app/                    # Main application package
│   ├── __init__.py        # Flask app initialization
│   ├── routes/            # Route handlers
│   ├── models/            # Database models
│   ├── services/          # Business logic
│   └── templates/         # HTML templates
├── docs/
│   ├── archive            # 
│   ├── deployement/       #
│   ├── development/       #
│   ├── features/          # 
│   ├── screenshots/       #  
│   └── testing/           # 
├── static/                # CSS, JS, images
├── tests/                 # Test suite
├── .env.example           # Environment template
├── requirements.txt       # Python dependencies
├── start.sh              # Startup script with SSL
└── app.py                # Application entry point
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

## Important Notes

- **HTTPS Required**: TeamSnap OAuth requires HTTPS for redirect URIs
- **Self-Signed Certificates**: Local development uses self-signed certificates (browser warnings expected)
- **TeamSnap API**: Requires approved application and API credentials from TeamSnap Developer Portal
- **Documentation**: See PROJECT_SUMMARY.md and HOSTING_GUIDE.md for detailed setup instructions
- **Todo Management**: Uses todo list management for tracking multi-user conversion and payment integration roadmap
- **Print Optimization**: Designs optimized for printing on field (landscape layouts, clear fonts)

## Roadmap

### Completed (MVP)
- ✅ TeamSnap OAuth integration
- ✅ 3-lineup generation with pitcher rotation
- ✅ Visual baseball diamond graphics
- ✅ Print-friendly layouts
- ✅ Position preference handling

### Planned Features
- 🔲 Multi-user/multi-tenant architecture
- 🔲 Payment integration (subscription-based)
- 🔲 Advanced lineup optimization algorithms
- 🔲 Season-long statistics tracking
- 🔲 Mobile-responsive design improvements
- 🔲 Additional sports support (softball, T-ball)
