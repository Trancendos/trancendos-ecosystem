#!/usr/bin/env python3
"""
Trancendos Ecosystem - Auto-Deployment Script
Handles complete deployment setup, workflow enablement, and service orchestration
"""

import os
import sys
import json
import time
import requests
import subprocess
from pathlib import Path
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('deployment.log')
    ]
)
logger = logging.getLogger(__name__)

class EcosystemDeployer:
    def __init__(self):
        self.repo_owner = 'Trancendos'
        self.repo_name = 'trancendos-ecosystem'
        self.github_token = os.environ.get('GITHUB_TOKEN', '')
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        logger.info("🔍 Checking prerequisites...")
        
        # Check GitHub token
        if not self.github_token:
            logger.error("❌ GITHUB_TOKEN environment variable not set")
            logger.info("Please set it with: export GITHUB_TOKEN=your_token_here")
            return False
            
        # Test GitHub API access
        try:
            response = requests.get(
                f"{self.base_url}/user",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                user_info = response.json()
                logger.info(f"✅ Authenticated as: {user_info['login']}")
            else:
                logger.error(f"❌ GitHub API error: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to connect to GitHub API: {e}")
            return False
            
        # Check if we can access the repository
        try:
            response = requests.get(
                f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}",
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                repo_info = response.json()
                logger.info(f"✅ Repository access confirmed: {repo_info['full_name']}")
            else:
                logger.error(f"❌ Cannot access repository: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"❌ Failed to access repository: {e}")
            return False
            
        logger.info("✅ All prerequisites met")
        return True
    
    def enable_github_actions(self):
        """Enable GitHub Actions for the repository"""
        logger.info("💫 Enabling GitHub Actions...")
        
        # Enable Actions
        response = requests.put(
            f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/actions/permissions",
            headers=self.headers,
            json={
                "enabled": True,
                "allowed_actions": "all"
            },
            timeout=10
        )
        
        if response.status_code in [200, 204]:
            logger.info("✅ GitHub Actions enabled")
            return True
        else:
            logger.error(f"❌ Failed to enable Actions: {response.status_code} - {response.text}")
            return False
    
    def setup_environments(self):
        """Set up deployment environments"""
        logger.info("🌍 Setting up deployment environments...")
        
        environments = {
            'staging': {
                'wait_timer': 0,
                'reviewers': [],
                'deployment_branch_policy': {
                    'protected_branches': False,
                    'custom_branch_policies': True
                }
            },
            'production': {
                'wait_timer': 300,  # 5 minute wait
                'reviewers': [],
                'deployment_branch_policy': {
                    'protected_branches': True,
                    'custom_branch_policies': False
                }
            }
        }
        
        success_count = 0
        for env_name, config in environments.items():
            response = requests.put(
                f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/environments/{env_name}",
                headers=self.headers,
                json=config,
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                logger.info(f"✅ Environment '{env_name}' configured")
                success_count += 1
            else:
                logger.warning(f"⚠️ Failed to create environment '{env_name}': {response.status_code}")
        
        logger.info(f"✅ {success_count}/{len(environments)} environments configured")
        return success_count > 0
    
    def generate_and_set_secrets(self):
        """Generate secrets and set them in GitHub repository"""
        logger.info("🔐 Generating and setting repository secrets...")
        
        # Import the secret manager
        sys.path.append(str(Path(__file__).parent))
        try:
            from generate_secrets import SecretManager
        except ImportError:
            logger.error("❌ Cannot import SecretManager - ensure generate-secrets.py exists")
            return False
        
        # Generate secrets for staging environment
        manager = SecretManager('staging')
        secrets = manager.generate_all_secrets()
        
        # Set secrets in GitHub repository
        success_count = 0
        for key, value in secrets.items():
            # Skip placeholder values
            if 'your_' in str(value) and '_here' in str(value):
                logger.info(f"⏭️ Skipping placeholder secret: {key}")
                continue
                
            # Set the secret
            response = requests.put(
                f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/actions/secrets/{key}",
                headers=self.headers,
                json={
                    "encrypted_value": self._encrypt_secret(value),
                    "key_id": self._get_public_key()["key_id"]
                },
                timeout=10
            )
            
            if response.status_code in [200, 201, 204]:
                logger.info(f"✅ Secret set: {key}")
                success_count += 1
            else:
                logger.error(f"❌ Failed to set secret {key}: {response.status_code}")
        
        logger.info(f"✅ {success_count} secrets configured successfully")
        return success_count > 0
    
    def _get_public_key(self):
        """Get repository public key for secret encryption"""
        response = requests.get(
            f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/actions/secrets/public-key",
            headers=self.headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to get public key: {response.status_code}")
    
    def _encrypt_secret(self, secret_value):
        """Encrypt secret value using repository public key"""
        try:
            from nacl import encoding, public
        except ImportError:
            logger.error("❌ PyNaCl not available - installing...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyNaCl'], check=True)
            from nacl import encoding, public
        
        public_key_info = self._get_public_key()
        public_key = public.PublicKey(public_key_info["key"].encode("utf-8"), encoding.Base64Encoder())
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return encoding.Base64Encoder().encode(encrypted).decode("utf-8")
    
    def trigger_workflows(self):
        """Trigger initial workflow runs"""
        logger.info("🚀 Triggering initial workflow runs...")
        
        # Wait a bit for workflows to be recognized
        logger.info("Waiting for workflows to be recognized...")
        time.sleep(10)
        
        # Get list of workflows
        response = requests.get(
            f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/actions/workflows",
            headers=self.headers,
            timeout=10
        )
        
        if response.status_code != 200:
            logger.error(f"❌ Failed to get workflows: {response.status_code}")
            return False
            
        workflows = response.json().get('workflows', [])
        logger.info(f"Found {len(workflows)} workflows")
        
        # Trigger specific workflows
        triggered_count = 0
        for workflow in workflows:
            workflow_name = workflow['name']
            workflow_id = workflow['id']
            
            # Skip if workflow is disabled
            if workflow['state'] == 'disabled_manually':
                logger.info(f"⏭️ Skipping disabled workflow: {workflow_name}")
                continue
            
            # Prepare workflow inputs based on workflow name
            inputs = {}
            if 'ecosystem-deploy' in workflow['path']:
                inputs = {
                    'environment': 'staging',
                    'services': 'all'
                }
            elif 'service-orchestration' in workflow['path']:
                inputs = {
                    'action': 'health-check',
                    'target_environment': 'staging',
                    'services': 'all'
                }
            
            # Trigger workflow
            response = requests.post(
                f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/actions/workflows/{workflow_id}/dispatches",
                headers=self.headers,
                json={
                    'ref': 'main',
                    'inputs': inputs
                },
                timeout=10
            )
            
            if response.status_code == 204:
                logger.info(f"✅ Triggered workflow: {workflow_name}")
                triggered_count += 1
            else:
                logger.warning(f"⚠️ Failed to trigger {workflow_name}: {response.status_code}")
        
        logger.info(f"✅ Triggered {triggered_count} workflows")
        return triggered_count > 0
    
    def setup_branch_protection(self):
        """Set up branch protection rules"""
        logger.info("🛡️ Setting up branch protection...")
        
        protection_config = {
            "required_status_checks": {
                "strict": True,
                "contexts": ["build-and-test"]
            },
            "enforce_admins": False,
            "required_pull_request_reviews": {
                "required_approving_review_count": 1,
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": False
            },
            "restrictions": None,
            "allow_force_pushes": False,
            "allow_deletions": False
        }
        
        response = requests.put(
            f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/branches/main/protection",
            headers=self.headers,
            json=protection_config,
            timeout=10
        )
        
        if response.status_code == 200:
            logger.info("✅ Branch protection configured")
            return True
        else:
            logger.warning(f"⚠️ Failed to set branch protection: {response.status_code}")
            return False
    
    def monitor_deployment(self, timeout_minutes=10):
        """Monitor the deployment process"""
        logger.info(f"📊 Monitoring deployment (timeout: {timeout_minutes} minutes)...")
        
        start_time = datetime.now()
        timeout_seconds = timeout_minutes * 60
        
        while True:
            elapsed = (datetime.now() - start_time).total_seconds()
            if elapsed > timeout_seconds:
                logger.warning("⚠️ Monitoring timeout reached")
                break
            
            # Get workflow runs
            response = requests.get(
                f"{self.base_url}/repos/{self.repo_owner}/{self.repo_name}/actions/runs",
                headers=self.headers,
                params={'per_page': 5},
                timeout=10
            )
            
            if response.status_code == 200:
                runs = response.json().get('workflow_runs', [])
                
                if runs:
                    latest_run = runs[0]
                    status = latest_run['status']
                    conclusion = latest_run['conclusion']
                    
                    logger.info(f"Latest run status: {status}, conclusion: {conclusion}")
                    
                    if status == 'completed':
                        if conclusion == 'success':
                            logger.info("✅ Deployment completed successfully!")
                            return True
                        else:
                            logger.error(f"❌ Deployment failed with conclusion: {conclusion}")
                            return False
            
            time.sleep(30)  # Wait 30 seconds before checking again
        
        logger.info("ℹ️ Monitoring completed (may still be running)")
        return True
    
    def deploy(self):
        """Execute the complete deployment process"""
        logger.info("🚀 Starting Trancendos Ecosystem deployment...")
        start_time = datetime.now()
        
        steps = [
            ("Prerequisites", self.check_prerequisites),
            ("Enable Actions", self.enable_github_actions),
            ("Setup Environments", self.setup_environments),
            ("Generate Secrets", self.generate_and_set_secrets),
            ("Trigger Workflows", self.trigger_workflows),
            ("Branch Protection", self.setup_branch_protection),
            ("Monitor Deployment", self.monitor_deployment)
        ]
        
        results = {}
        for step_name, step_func in steps:
            logger.info(f"\n➡️ Executing: {step_name}")
            try:
                results[step_name] = step_func()
                if results[step_name]:
                    logger.info(f"✅ {step_name} completed successfully")
                else:
                    logger.error(f"❌ {step_name} failed")
                    if step_name in ["Prerequisites", "Enable Actions"]:
                        logger.error("Critical step failed - stopping deployment")
                        return False
            except Exception as e:
                logger.error(f"❌ {step_name} error: {e}")
                results[step_name] = False
        
        # Summary
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info("\n" + "="*50)
        logger.info("🎉 DEPLOYMENT SUMMARY")
        logger.info("="*50)
        
        success_count = sum(1 for result in results.values() if result)
        total_steps = len(steps)
        
        for step_name, result in results.items():
            status = "✅" if result else "❌"
            logger.info(f"{status} {step_name}")
        
        logger.info(f"\n📊 Results: {success_count}/{total_steps} steps successful")
        logger.info(f"⏱️ Duration: {duration.total_seconds():.1f} seconds")
        
        if success_count >= total_steps - 2:  # Allow some optional steps to fail
            logger.info("🎉 Deployment completed successfully!")
            logger.info(f"\n🔗 Repository: https://github.com/{self.repo_owner}/{self.repo_name}")
            logger.info(f"💫 Actions: https://github.com/{self.repo_owner}/{self.repo_name}/actions")
            return True
        else:
            logger.error("❌ Deployment completed with errors")
            return False

def main():
    """Main execution function"""
    deployer = EcosystemDeployer()
    
    # Check for GitHub token
    if not os.environ.get('GITHUB_TOKEN'):
        print("❌ GITHUB_TOKEN environment variable is required")
        print("Please set it with: export GITHUB_TOKEN=your_github_token")
        print("Get a token from: https://github.com/settings/tokens")
        sys.exit(1)
    
    success = deployer.deploy()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()