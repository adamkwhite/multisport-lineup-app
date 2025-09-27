# Baseball Lineup Management App - Claude Context

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

## Key Features

- TeamSnap OAuth integration for team/player data
- 3-lineup generation with pitcher rotation (2 innings max per pitcher)
- Visual baseball diamond field graphics
- Print-friendly layouts for field use
- Position preferences (pitcher, catcher, any position)
- Player randomization across lineups for development

## Development Setup

### Required Environment
```bash
# Install dependencies
pip install -r requirements.txt

# Copy .env.example to .env and add your TeamSnap API credentials
# IMPORTANT: Add FLASK_SSL=true to .env file for HTTPS support
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

## API Integration

### TeamSnap API
- **OAuth 2.0** authentication required
- **HTTPS mandatory** for redirect URIs
- **Rate limiting** considerations for production deployment
- **Collection+JSON** format for API responses
- See `.env.example` for required environment variables

## Important Notes

- Requires TeamSnap API credentials and HTTPS setup for OAuth
- See PROJECT_SUMMARY.md and HOSTING_GUIDE.md for detailed setup instructions
- Uses todo list management for tracking multi-user conversion and payment integration roadmap
- Print-friendly designs optimized for field use

## Deployment

- Designed for Heroku deployment
- Plans for multi-user SaaS conversion
- Payment integration roadmap in development