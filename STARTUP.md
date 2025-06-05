# Baseball Lineup App - Startup Instructions

## Quick Start

### Option 1: HTTP (Recommended for Local Development)
```bash
cd /home/adam/Code/baseball-lineup-app
PORT=3000 python3 app.py
```
Then open: **http://localhost:3000**

### Option 2: HTTPS (Required for TeamSnap OAuth in Production)
```bash
cd /home/adam/Code/baseball-lineup-app
FLASK_SSL=true python3 app.py
```
Then open: **https://localhost:5000** (accept security warnings for self-signed certificate)

## Prerequisites

1. **Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **TeamSnap API Credentials**
   - Copy `.env.example` to `.env`
   - Add your TeamSnap API credentials to `.env`
   - See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for setup details

3. **SSL Certificates (for HTTPS mode)**
   - Certificates already exist: `cert.pem` and `key.pem`
   - Generated with: `./create_ssl_cert.sh`

## Troubleshooting

### Connection Refused
- Make sure no other process is using the port
- Kill existing processes: `pkill -f "python.*app.py"`
- Try a different port: `PORT=8080 python3 app.py`

### SSL Certificate Warnings
- Click "Advanced" → "Proceed to localhost (unsafe)" in your browser
- Or use HTTP mode instead with `PORT=3000 python3 app.py`

### TeamSnap Authentication Issues
- Verify `.env` file has correct API credentials
- Check that `TEAMSNAP_CLIENT_ID` and `TEAMSNAP_CLIENT_SECRET` are set
- Ensure redirect URI matches what's configured in TeamSnap Developer Portal

## Application Features

Once running, you can:
1. **Select a Team** - Loads from your TeamSnap account
2. **Choose a Game** - Shows upcoming games with availability
3. **Generate Lineups** - Creates 3 optimized lineups with:
   - 6-inning game structure
   - Pitcher rotation (max 2 innings per pitcher)
   - Position preferences respected
   - Player randomization for development
4. **Print Lineups** - Formatted for field use

## Environment Variables

- `PORT` - Server port (default: 5000)
- `FLASK_SSL` - Enable HTTPS mode (set to "true")
- `FLASK_DEBUG` - Debug mode (default: "true")
- `TEAMSNAP_CLIENT_ID` - TeamSnap OAuth client ID
- `TEAMSNAP_CLIENT_SECRET` - TeamSnap OAuth client secret

## Production Deployment

For production (Heroku), use HTTPS mode:
- SSL is required for TeamSnap OAuth redirects
- Set `FLASK_SSL=true` in environment variables
- Configure proper domain in TeamSnap Developer Portal

See [HOSTING_GUIDE.md](HOSTING_GUIDE.md) for detailed deployment instructions.