#!/bin/bash

# Baseball Lineup Manager Start Script
echo "🚀 Starting Baseball Lineup Manager..."

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
if [ ! -f "cert.pem" ] || [ ! -f "key.pem" ]; then
    echo "🔐 Creating SSL certificates for HTTPS..."
    ./create_ssl_cert.sh
fi

echo "🌐 Starting Flask app on https://localhost:5000"
echo "⚠️  Your browser will show a security warning for self-signed certificate"
echo "📝 Press Ctrl+C to stop"

python3 app.py