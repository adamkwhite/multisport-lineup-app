#!/bin/bash

# Create self-signed SSL certificate for development
echo "🔐 Creating SSL certificate for development..."

# Generate private key and certificate
openssl req -x509 -newkey rsa:4096 -nodes -out certs/cert.pem -keyout certs/key.pem -days 365 \
    -subj "/C=US/ST=State/L=City/O=Organization/OU=OrgUnit/CN=localhost"

echo "✅ SSL certificate created (certs/cert.pem, certs/key.pem)"
echo "⚠️  This is a self-signed certificate for development only"
echo "🌐 Your browser will show a security warning - click 'Advanced' and 'Proceed to localhost'"