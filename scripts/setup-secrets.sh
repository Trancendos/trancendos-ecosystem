#!/bin/bash
# 🔐 Secure Secrets Setup for Trancendos Ecosystem
# 🚨 CRITICAL: Run this script before deploying hardened configuration

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔐 Trancendos Ecosystem - Secure Secrets Setup${NC}"
echo -e "${YELLOW}⚠️  CRITICAL: This will generate production secrets${NC}"
echo ""

# Create secrets directory
SECRETS_DIR="./secrets"
if [[ ! -d "$SECRETS_DIR" ]]; then
    echo -e "${BLUE}Creating secrets directory...${NC}"
    mkdir -p "$SECRETS_DIR"
    chmod 700 "$SECRETS_DIR"
fi

# Function to generate secure random string
generate_secret() {
    openssl rand -base64 32 | tr -d "\n"
}

# Function to generate JWT secret
generate_jwt_secret() {
    openssl rand -base64 64 | tr -d "\n"
}

# Function to generate encryption key
generate_encryption_key() {
    openssl rand -hex 32 | tr -d "\n"
}

echo -e "${GREEN}🔑 Generating secure secrets...${NC}"

# Database secrets
echo -e "${BLUE}Generating database credentials...${NC}"
generate_secret > "$SECRETS_DIR/postgres_password.txt"
generate_secret > "$SECRETS_DIR/redis_password.txt"
echo "Database secrets generated ✓"

# Application secrets
echo -e "${BLUE}Generating application secrets...${NC}"
generate_jwt_secret > "$SECRETS_DIR/jwt_secret.txt"
generate_encryption_key > "$SECRETS_DIR/encryption_key.txt"
generate_secret > "$SECRETS_DIR/api_encryption_key.txt"
generate_secret > "$SECRETS_DIR/ml_model_key.txt"
echo "Application secrets generated ✓"

# Monitoring secrets
echo -e "${BLUE}Generating monitoring secrets...${NC}"
generate_secret > "$SECRETS_DIR/grafana_password.txt"
generate_secret > "$SECRETS_DIR/grafana_secret.txt"
echo "Monitoring secrets generated ✓"

# Set proper permissions
echo -e "${BLUE}Setting secure file permissions...${NC}"
chmod 600 "$SECRETS_DIR"/*.txt
chown root:root "$SECRETS_DIR"/*.txt 2>/dev/null || true

echo ""
echo -e "${GREEN}🎉 All secrets generated successfully!${NC}"
echo ""
echo -e "${YELLOW}🛡️  SECURITY REMINDERS:${NC}"
echo "1. 🚫 NEVER commit secrets directory to Git"
echo "2. 📝 Backup secrets to secure location"
echo "3. 🔄 Rotate secrets regularly (every 90 days)"
echo "4. 📊 Monitor secret access and usage"
echo "5. 🔒 Use different secrets for each environment"
echo ""
echo -e "${BLUE}Generated files:${NC}"
ls -la "$SECRETS_DIR"/
echo ""
echo -e "${GREEN}✅ Ready to deploy with: docker-compose -f docker-compose.secure.yml up -d${NC}"

# Create .gitignore entry if it doesn't exist
if ! grep -q "secrets/" .gitignore 2>/dev/null; then
    echo -e "${BLUE}Adding secrets directory to .gitignore...${NC}"
    echo "" >> .gitignore
    echo "# Security - Never commit secrets" >> .gitignore
    echo "secrets/" >> .gitignore
    echo "*.key" >> .gitignore
    echo "*.pem" >> .gitignore
    echo "*.p12" >> .gitignore
    echo ".env" >> .gitignore
    echo ".env.local" >> .gitignore
    echo ".env.production" >> .gitignore
fi

# Display secret verification
echo -e "${YELLOW}🔍 Secret verification:${NC}"
echo "PostgreSQL password length: $(wc -c < "$SECRETS_DIR/postgres_password.txt") characters"
echo "JWT secret length: $(wc -c < "$SECRETS_DIR/jwt_secret.txt") characters"
echo "Encryption key length: $(wc -c < "$SECRETS_DIR/encryption_key.txt") characters"

echo ""
echo -e "${GREEN}🔐 Secrets setup completed successfully!${NC}"
