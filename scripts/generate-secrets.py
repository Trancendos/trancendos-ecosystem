#!/usr/bin/env python3
"""
Trancendos Ecosystem - Secret Generation and Management
Generates secure secrets for all services and manages environment configurations
"""

import os
import secrets
import string
import json
import subprocess
import base64
import hashlib
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecretManager:
    def __init__(self, environment='development'):
        self.environment = environment
        self.secrets = {}
        self.root_path = Path(__file__).parent.parent
        
    def generate_password(self, length=32, include_symbols=True):
        """Generate a cryptographically secure password"""
        alphabet = string.ascii_letters + string.digits
        if include_symbols:
            alphabet += "!@#$%^&*()-_=+[]{}|;:,.<>?"
        
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        return password
    
    def generate_jwt_secret(self):
        """Generate JWT secret key"""
        return base64.b64encode(secrets.token_bytes(64)).decode('utf-8')
    
    def generate_encryption_key(self):
        """Generate Fernet encryption key"""
        return Fernet.generate_key().decode('utf-8')
    
    def generate_api_key(self, prefix='', length=32):
        """Generate API key with optional prefix"""
        key_part = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(length))
        return f"{prefix}{'_' if prefix else ''}{key_part}"
    
    def generate_webhook_secret(self):
        """Generate webhook secret for secure payload verification"""
        return secrets.token_hex(32)
    
    def generate_database_url(self, host='localhost', port=5432, database='trancendos'):
        """Generate secure database URL"""
        username = 'trancendos'
        password = self.generate_password(24, include_symbols=False)
        return f"postgresql://{username}:{password}@{host}:{port}/{database}"
    
    def generate_all_secrets(self):
        """Generate all required secrets for the ecosystem"""
        logger.info(f"Generating secrets for {self.environment} environment")
        
        self.secrets = {
            # Database Configuration
            'POSTGRES_PASSWORD': self.generate_password(24),
            'DATABASE_URL': self.generate_database_url(),
            
            # Redis Configuration
            'REDIS_URL': 'redis://localhost:6379',
            'REDIS_PASSWORD': self.generate_password(16),
            
            # Security Configuration
            'JWT_SECRET': self.generate_jwt_secret(),
            'ENCRYPTION_KEY': self.generate_encryption_key(),
            'SESSION_SECRET': self.generate_password(32),
            'CSRF_SECRET': self.generate_password(24),
            
            # API Keys
            'INTERNAL_API_KEY': self.generate_api_key('TRNCD', 40),
            'WEBHOOK_SECRET': self.generate_webhook_secret(),
            
            # Monitoring Configuration
            'GRAFANA_PASSWORD': self.generate_password(16),
            'PROMETHEUS_PASSWORD': self.generate_password(16),
            
            # External Service Placeholders (to be filled manually)
            'STRIPE_API_KEY': 'sk_test_your_stripe_key_here',
            'STRIPE_WEBHOOK_SECRET': self.generate_webhook_secret(),
            'PLAID_CLIENT_ID': 'your_plaid_client_id_here',
            'PLAID_SECRET': 'your_plaid_secret_here',
            
            # Notification Services
            'SLACK_WEBHOOK': 'https://hooks.slack.com/your/webhook/url',
            'DISCORD_WEBHOOK': 'https://discord.com/api/webhooks/your/webhook',
            
            # Linear Integration
            'LINEAR_API_KEY': 'lin_api_your_key_here',
            'LINEAR_WEBHOOK_SECRET': self.generate_webhook_secret(),
            
            # Notion Integration
            'NOTION_API_KEY': 'secret_your_notion_key_here',
            'NOTION_DATABASE_ID': 'your_notion_database_id_here',
            
            # Email Configuration
            'SMTP_PASSWORD': self.generate_password(16),
            'SENDGRID_API_KEY': 'SG.your_sendgrid_key_here',
            
            # Cloud Storage
            'AWS_ACCESS_KEY_ID': 'AKIA_your_access_key_here',
            'AWS_SECRET_ACCESS_KEY': self.generate_password(40, include_symbols=False),
            'S3_BUCKET_NAME': f'trancendos-{self.environment}',
            
            # OAuth Configuration
            'GOOGLE_CLIENT_SECRET': self.generate_password(24, include_symbols=False),
            'GITHUB_CLIENT_SECRET': self.generate_password(32, include_symbols=False),
            
            # Rate Limiting
            'RATE_LIMIT_SECRET': self.generate_password(32),
            
            # Backup Encryption
            'BACKUP_ENCRYPTION_KEY': self.generate_encryption_key(),
        }
        
        # Environment-specific overrides
        if self.environment == 'production':
            self.secrets.update({
                'DATABASE_URL': self.generate_database_url('prod-db.trancendos.com', 5432),
                'REDIS_URL': 'redis://prod-redis.trancendos.com:6379',
            })
        elif self.environment == 'staging':
            self.secrets.update({
                'DATABASE_URL': self.generate_database_url('staging-db.trancendos.com', 5432),
                'REDIS_URL': 'redis://staging-redis.trancendos.com:6379',
            })
        
        return self.secrets
    
    def save_to_env_file(self, filename=None):
        """Save secrets to environment file"""
        if not filename:
            filename = f'.env.{self.environment}'
        
        env_path = self.root_path / filename
        
        with open(env_path, 'w') as f:
            f.write(f"# Trancendos Ecosystem - {self.environment.upper()} Environment\n")
            f.write(f"# Generated automatically on {os.popen('date').read().strip()}\n\n")
            
            # Group secrets by category
            categories = {
                'Database Configuration': ['POSTGRES_PASSWORD', 'DATABASE_URL'],
                'Redis Configuration': ['REDIS_URL', 'REDIS_PASSWORD'],
                'Security Configuration': ['JWT_SECRET', 'ENCRYPTION_KEY', 'SESSION_SECRET', 'CSRF_SECRET'],
                'API Configuration': ['INTERNAL_API_KEY', 'WEBHOOK_SECRET'],
                'Monitoring Configuration': ['GRAFANA_PASSWORD', 'PROMETHEUS_PASSWORD'],
                'External Services': ['STRIPE_API_KEY', 'STRIPE_WEBHOOK_SECRET', 'PLAID_CLIENT_ID', 'PLAID_SECRET'],
                'Notifications': ['SLACK_WEBHOOK', 'DISCORD_WEBHOOK'],
                'Integrations': ['LINEAR_API_KEY', 'LINEAR_WEBHOOK_SECRET', 'NOTION_API_KEY', 'NOTION_DATABASE_ID'],
                'Email Services': ['SMTP_PASSWORD', 'SENDGRID_API_KEY'],
                'Cloud Storage': ['AWS_ACCESS_KEY_ID', 'AWS_SECRET_ACCESS_KEY', 'S3_BUCKET_NAME'],
                'OAuth Services': ['GOOGLE_CLIENT_SECRET', 'GITHUB_CLIENT_SECRET'],
                'Performance': ['RATE_LIMIT_SECRET'],
                'Backup & Recovery': ['BACKUP_ENCRYPTION_KEY'],
            }
            
            for category, keys in categories.items():
                f.write(f"# {category}\n")
                for key in keys:
                    if key in self.secrets:
                        f.write(f"{key}={self.secrets[key]}\n")
                f.write("\n")
        
        logger.info(f"Secrets saved to {env_path}")
        return env_path
    
    def save_to_github_secrets(self, repo_owner, repo_name):
        """Save secrets to GitHub repository secrets using GitHub CLI"""
        logger.info("Saving secrets to GitHub repository...")
        
        # Check if gh CLI is available
        try:
            subprocess.run(['gh', '--version'], check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("GitHub CLI (gh) is not installed or not in PATH")
            return False
        
        success_count = 0
        for key, value in self.secrets.items():
            try:
                result = subprocess.run([
                    'gh', 'secret', 'set', key,
                    '--repo', f"{repo_owner}/{repo_name}",
                    '--body', value
                ], check=True, capture_output=True, text=True)
                
                logger.info(f"✅ Set secret: {key}")
                success_count += 1
            except subprocess.CalledProcessError as e:
                logger.error(f"❌ Failed to set secret {key}: {e.stderr}")
        
        logger.info(f"Successfully set {success_count}/{len(self.secrets)} secrets")
        return success_count == len(self.secrets)
    
    def generate_docker_secrets(self):
        """Generate Docker Swarm secrets configuration"""
        docker_secrets = {}
        
        for key, value in self.secrets.items():
            docker_secrets[key.lower()] = {
                'external': True,
                'name': f"trancendos_{self.environment}_{key.lower()}"
            }
        
        return docker_secrets
    
    def generate_kubernetes_secrets(self):
        """Generate Kubernetes secrets YAML"""
        import base64
        
        k8s_secrets = {
            'apiVersion': 'v1',
            'kind': 'Secret',
            'metadata': {
                'name': f'trancendos-{self.environment}-secrets',
                'namespace': 'default'
            },
            'type': 'Opaque',
            'data': {}
        }
        
        for key, value in self.secrets.items():
            k8s_secrets['data'][key] = base64.b64encode(value.encode()).decode()
        
        return k8s_secrets
    
    def encrypt_secrets_file(self, password, input_file, output_file=None):
        """Encrypt secrets file with password"""
        if not output_file:
            output_file = f"{input_file}.encrypted"
        
        # Derive key from password
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        
        # Encrypt file
        fernet = Fernet(key)
        with open(input_file, 'rb') as f:
            data = f.read()
        
        encrypted_data = fernet.encrypt(data)
        
        with open(output_file, 'wb') as f:
            f.write(salt + encrypted_data)
        
        logger.info(f"Encrypted secrets saved to {output_file}")
        return output_file

def main():
    parser = argparse.ArgumentParser(description='Generate and manage Trancendos Ecosystem secrets')
    parser.add_argument('--env', choices=['development', 'staging', 'production'], 
                        default='development', help='Environment to generate secrets for')
    parser.add_argument('--output', help='Output file name')
    parser.add_argument('--github-repo', help='GitHub repository (owner/repo) to set secrets')
    parser.add_argument('--encrypt', help='Password to encrypt the secrets file')
    parser.add_argument('--docker', action='store_true', help='Generate Docker secrets configuration')
    parser.add_argument('--kubernetes', action='store_true', help='Generate Kubernetes secrets YAML')
    
    args = parser.parse_args()
    
    # Generate secrets
    manager = SecretManager(args.env)
    secrets = manager.generate_all_secrets()
    
    # Save to environment file
    env_file = manager.save_to_env_file(args.output)
    
    # Encrypt if requested
    if args.encrypt:
        manager.encrypt_secrets_file(args.encrypt, env_file)
    
    # Set GitHub secrets if requested
    if args.github_repo:
        owner, repo = args.github_repo.split('/')
        manager.save_to_github_secrets(owner, repo)
    
    # Generate Docker configuration
    if args.docker:
        docker_config = manager.generate_docker_secrets()
        with open(f'docker-secrets-{args.env}.json', 'w') as f:
            json.dump(docker_config, f, indent=2)
        logger.info(f"Docker secrets configuration saved to docker-secrets-{args.env}.json")
    
    # Generate Kubernetes configuration
    if args.kubernetes:
        k8s_config = manager.generate_kubernetes_secrets()
        with open(f'k8s-secrets-{args.env}.yaml', 'w') as f:
            import yaml
            yaml.dump(k8s_config, f, default_flow_style=False)
        logger.info(f"Kubernetes secrets configuration saved to k8s-secrets-{args.env}.yaml")
    
    print(f"\n🎉 Generated {len(secrets)} secrets for {args.env} environment!")
    print(f"📁 Environment file: {env_file}")
    print("\n⚠️  Remember to:")
    print("   1. Update external API keys with real values")
    print("   2. Never commit .env files to version control")
    print("   3. Use different secrets for each environment")
    print("   4. Rotate secrets regularly")

if __name__ == '__main__':
    main()