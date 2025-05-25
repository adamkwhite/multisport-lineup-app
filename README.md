# Baseball Lineup Manager

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
cd baseball-lineup-app
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

## Deployment

Can be deployed to:
- Heroku
- AWS EC2 (like your SBTM tool)
- Local development server