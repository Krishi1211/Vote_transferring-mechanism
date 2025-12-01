#!/bin/bash
# Generate self-signed SSL certificate for development
# For production, use Let's Encrypt or a proper CA

echo "Generating self-signed SSL certificate for development..."

openssl req -x509 -newkey rsa:4096 -nodes \
  -out cert.pem -keyout key.pem -days 365 \
  -subj "/C=US/ST=California/L=Davis/O=SecureVoteSystem/CN=localhost"

echo "Certificate generated:"
echo "  - cert.pem (certificate)"
echo "  - key.pem (private key)"
echo ""
echo "Add to .env file:"
echo "SSL_CERT_PATH=$(pwd)/cert.pem"
echo "SSL_KEY_PATH=$(pwd)/key.pem"
