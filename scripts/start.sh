#!/bin/bash

# Multi-Sport Lineup Manager Start Script
echo "🚀 Starting Multi-Sport Lineup Manager..."

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and add your TeamSnap API credentials"
    exit 1
fi

# Check if required variables are set
if grep -q "your_client_id_here" .env; then
    echo "❌ Error: Please update .env with your actual TeamSnap API credentials"
    echo "Edit .env and replace:"
    echo "  TEAMSNAP_CLIENT_ID=your_actual_client_id"
    echo "  TEAMSNAP_CLIENT_SECRET=your_actual_client_secret"
    exit 1
fi

echo "✅ Environment configured"

# Check if SSL certificates exist
if [ ! -f "certs/cert.pem" ] || [ ! -f "certs/key.pem" ]; then
    echo "🔐 Creating SSL certificates for HTTPS..."
    ./scripts/create_ssl_cert.sh
fi

PORT=${PORT:-5001}  # Default to 5001 if not set
echo "🌐 Starting Flask app on https://localhost:$PORT"
echo "⚠️  Your browser will show a security warning for self-signed certificate"
echo "📝 Press Ctrl+C to stop"

./lineup-venv/bin/python app.py