# Baseball Lineup Manager

[![Quality Gate Status](http://44.206.255.230:9000/api/project_badges/measure?project=baseball-lineup-app&metric=alert_status)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Coverage](http://44.206.255.230:9000/api/project_badges/measure?project=baseball-lineup-app&metric=coverage)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Bugs](http://44.206.255.230:9000/api/project_badges/measure?project=baseball-lineup-app&metric=bugs)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Vulnerabilities](http://44.206.255.230:9000/api/project_badges/measure?project=baseball-lineup-app&metric=vulnerabilities)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Code Smells](http://44.206.255.230:9000/api/project_badges/measure?project=baseball-lineup-app&metric=code_smells)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Security Rating](http://44.206.255.230:9000/api/project_badges/measure?project=baseball-lineup-app&metric=security_rating)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Maintainability Rating](http://44.206.255.230:9000/api/project_badges/measure?project=baseball-lineup-app&metric=sqale_rating)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Reliability Rating](http://44.206.255.230:9000/api/project_badges/measure?project=baseball-lineup-app&metric=reliability_rating)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Lines of Code](http://44.206.255.230:9000/api/project_badges/measure?project=baseball-lineup-app&metric=ncloc)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Duplicated Lines (%)](http://44.206.255.230:9000/api/project_badges/measure?project=baseball-lineup-app&metric=duplicated_lines_density)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)
[![Technical Debt](http://44.206.255.230:9000/api/project_badges/measure?project=baseball-lineup-app&metric=sqale_index)](http://44.206.255.230:9000/dashboard?id=baseball-lineup-app)

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