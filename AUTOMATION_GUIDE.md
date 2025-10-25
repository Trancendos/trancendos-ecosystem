# 🤖 Trancendos Ecosystem - Automation & Deployment Guide

This guide explains how to use the comprehensive automation system deployed to your GitHub repository.

## 🚀 Quick Start - Deploy Everything Now!

The automation is **already deployed** to your repository! Here's how to activate it:

### Option 1: Automatic Setup (Recommended)

```bash
# Set your GitHub token (get from https://github.com/settings/tokens)
export GITHUB_TOKEN=your_github_token_here

# Run the auto-deployment script
python3 scripts/auto-deploy.py
```

This will:
- ✅ Enable GitHub Actions
- ✅ Generate and set all secrets automatically
- ✅ Configure deployment environments
- ✅ Set up branch protection
- ✅ Trigger initial workflow runs
- ✅ Monitor deployment progress

### Option 2: Manual Setup

```bash
# Make the script executable
chmod +x scripts/enable-workflows.sh

# Run the enablement script
./scripts/enable-workflows.sh
```

## 📋 What's Already Deployed

### 🔧 Workflows Created

| Workflow | Purpose | Trigger |
|----------|---------|----------|
| **[ecosystem-deploy.yml](https://github.com/Trancendos/trancendos-ecosystem/blob/main/.github/workflows/ecosystem-deploy.yml)** | Complete CI/CD pipeline | Push to main/develop, Manual |
| **[service-orchestration.yml](https://github.com/Trancendos/trancendos-ecosystem/blob/main/.github/workflows/service-orchestration.yml)** | Service automation & monitoring | Schedule (daily), Manual |

### 🛠️ Scripts Available

| Script | Purpose | Usage |
|--------|---------|-------|
| **[auto-deploy.py](https://github.com/Trancendos/trancendos-ecosystem/blob/main/scripts/auto-deploy.py)** | Complete deployment automation | `python3 scripts/auto-deploy.py` |
| **[generate-secrets.py](https://github.com/Trancendos/trancendos-ecosystem/blob/main/scripts/generate-secrets.py)** | Secure secret generation | `python3 scripts/generate-secrets.py --env staging` |
| **[enable-workflows.sh](https://github.com/Trancendos/trancendos-ecosystem/blob/main/scripts/enable-workflows.sh)** | GitHub Actions enablement | `./scripts/enable-workflows.sh` |

## 🎯 Automation Features

### 🔄 Continuous Integration/Deployment

**Ecosystem Deploy Workflow** handles:
- **Smart change detection** - Only builds modified services
- **Multi-environment deployment** - Staging → Production pipeline
- **Automated secret generation** - Creates secure credentials
- **Security scanning** - Trivy vulnerability analysis
- **Container registry** - Automatic Docker image builds
- **Health monitoring** - Post-deployment verification

### 🎼 Service Orchestration

**Service Orchestration Workflow** provides:
- **Scheduled maintenance** - Daily at 2 AM UTC
- **Health monitoring** - Every 6 hours
- **Auto-scaling** - Resource-based scaling decisions
- **Dependency updates** - Automated with PR creation
- **Backup operations** - Database and configuration backups
- **Security operations** - Vulnerability scans and secret rotation

### 🔐 Secret Management

**Automated secret generation** includes:
- Database credentials (PostgreSQL)
- API keys and tokens
- Encryption keys (JWT, Fernet)
- Webhook secrets
- OAuth configuration
- External service placeholders

## 📊 Monitoring & Notifications

### 🔔 Slack Integration
Set up Slack notifications by adding your webhook URL:
```bash
gh secret set SLACK_WEBHOOK --body "https://hooks.slack.com/your/webhook/url"
```

### 📈 Health Monitoring
Automated health checks for:
- Backend API endpoints
- Frontend application
- Database connectivity
- External service integrations

### 🚨 Alert System
Automated alerts for:
- Deployment failures
- Health check failures
- Security vulnerabilities
- Resource usage spikes

## 🛠️ Manual Operations

### Trigger Specific Actions

```bash
# Trigger full deployment
gh workflow run ecosystem-deploy.yml -f environment=staging -f services=all

# Trigger health check
gh workflow run service-orchestration.yml -f action=health-check -f target_environment=staging

# Trigger scaling operation
gh workflow run service-orchestration.yml -f action=scale-services -f target_environment=production

# Rotate all secrets
gh workflow run service-orchestration.yml -f action=rotate-secrets -f target_environment=production
```

### Generate Secrets Manually

```bash
# Generate staging secrets
python3 scripts/generate-secrets.py --env staging --github-repo Trancendos/trancendos-ecosystem

# Generate production secrets with encryption
python3 scripts/generate-secrets.py --env production --encrypt mypassword

# Generate Docker/Kubernetes configurations
python3 scripts/generate-secrets.py --docker --kubernetes
```

## 🔧 Configuration

### Required Secrets

Set these in your [repository secrets](https://github.com/Trancendos/trancendos-ecosystem/settings/secrets/actions):

#### Deployment Platforms
```bash
RAILWAY_TOKEN=your_railway_token
RENDER_API_KEY=your_render_api_key
HEROKU_API_KEY=your_heroku_api_key
```

#### External Services
```bash
STRIPE_API_KEY=sk_live_your_stripe_key
PLAID_CLIENT_ID=your_plaid_client_id
PLAID_SECRET=your_plaid_secret
NOTION_API_KEY=secret_your_notion_key
LINEAR_API_KEY=lin_api_your_key
```

#### Monitoring & Notifications
```bash
SLACK_WEBHOOK=https://hooks.slack.com/your/webhook
STAGING_URL=https://your-staging-domain.com
PROD_BACKEND_URL=https://your-production-api.com
STAGING_BACKEND_URL=https://your-staging-api.com
```

### Environment Configuration

**Staging Environment:**
- Auto-deploys from `develop` branch
- No manual approval required
- Health checks every 6 hours
- Automated testing and security scans

**Production Environment:**
- Deploys from `main` branch only
- 5-minute wait timer
- Enhanced security scanning
- Automated rollback on failure

## 🏗️ Deployment Targets

Your ecosystem supports multiple deployment platforms:

### ☁️ Railway
- **Configuration:** `railway.json`
- **Features:** Auto-scaling, built-in monitoring
- **Best for:** Backend services, databases

### 🎨 Render
- **Configuration:** `render.yaml`
- **Features:** Static sites, web services
- **Best for:** Frontend applications, APIs

### 🐳 Docker
- **Configuration:** `docker-compose.yml`, `Dockerfile`
- **Features:** Containerized deployment
- **Best for:** Local development, self-hosted

### 🐙 GitHub Pages
- **Configuration:** Automated via workflows
- **Features:** Static site hosting
- **Best for:** Documentation, frontend demos

## 🚀 Scaling Operations

### Automated Scaling Triggers
- **CPU usage** > 80%
- **Memory usage** > 85%
- **Response time** > 2 seconds
- **Error rate** > 5%

### Manual Scaling
```bash
# Scale specific services
gh workflow run service-orchestration.yml \
  -f action=scale-services \
  -f target_environment=production \
  -f services=backend,frontend
```

## 🔄 Backup & Recovery

### Automated Backups
- **Database backups** - Daily PostgreSQL dumps
- **Configuration backups** - All config files
- **Code backups** - Repository snapshots
- **Secret backups** - Encrypted credential stores

### Manual Backup
```bash
# Trigger backup operation
gh workflow run service-orchestration.yml -f action=backup-data -f target_environment=production
```

## 📚 Advanced Usage

### Custom Workflow Triggers

**Webhook Integration:**
```bash
# Set up webhook for external triggers
curl -X POST "https://api.github.com/repos/Trancendos/trancendos-ecosystem/dispatches" \
  -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.everest-preview+json" \
  -d '{"event_type":"deploy-staging"}'
```

**API Integration:**
```python
import requests

# Trigger deployment via API
response = requests.post(
    "https://api.github.com/repos/Trancendos/trancendos-ecosystem/actions/workflows/ecosystem-deploy.yml/dispatches",
    headers={
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github+json"
    },
    json={
        "ref": "main",
        "inputs": {
            "environment": "production",
            "services": "backend,frontend"
        }
    }
)
```

### Multi-Repository Management

Extend automation to other repositories:

```bash
# Copy workflows to other repos
cp -r .github/workflows/* ../other-repo/.github/workflows/
cp scripts/generate-secrets.py ../other-repo/scripts/

# Adapt for specific repository
sed -i 's/trancendos-ecosystem/other-repo/g' ../other-repo/.github/workflows/*.yml
```

## 🐛 Troubleshooting

### Common Issues

**Workflows not running:**
```bash
# Check if Actions are enabled
gh api repos/Trancendos/trancendos-ecosystem/actions/permissions

# Enable Actions
gh api --method PUT repos/Trancendos/trancendos-ecosystem/actions/permissions \
  -f enabled=true -f allowed_actions=all
```

**Secret generation fails:**
```bash
# Install required dependencies
pip3 install cryptography PyNaCl

# Generate secrets manually
python3 scripts/generate-secrets.py --env staging
```

**Deployment failures:**
```bash
# Check workflow logs
gh run list --limit 5
gh run view [run-id] --log

# Re-run failed jobs
gh run rerun [run-id] --failed
```

### Debug Mode

```bash
# Enable debug logging
gh secret set ACTIONS_STEP_DEBUG --body "true"
gh secret set ACTIONS_RUNNER_DEBUG --body "true"
```

## 📞 Support & Monitoring

### Live Monitoring

- **Actions Tab:** [View workflow runs](https://github.com/Trancendos/trancendos-ecosystem/actions)
- **Deployments:** [View deployment history](https://github.com/Trancendos/trancendos-ecosystem/deployments)
- **Security:** [View security overview](https://github.com/Trancendos/trancendos-ecosystem/security)

### Status Badges

Add these to your README:

```markdown
[![Ecosystem Deploy](https://github.com/Trancendos/trancendos-ecosystem/workflows/Trancendos%20Ecosystem%20CI/CD/badge.svg)](https://github.com/Trancendos/trancendos-ecosystem/actions)
[![Service Health](https://github.com/Trancendos/trancendos-ecosystem/workflows/Service%20Orchestration%20%26%20Automation/badge.svg)](https://github.com/Trancendos/trancendos-ecosystem/actions)
```

---

## 🎉 You're All Set!

Your complete automation system is now deployed! The workflows will:

✅ **Automatically deploy** on every push to main/develop  
✅ **Monitor health** every 6 hours  
✅ **Scale services** based on resource usage  
✅ **Update dependencies** and create PRs  
✅ **Backup data** daily  
✅ **Rotate secrets** on schedule  
✅ **Send notifications** to Slack  

**Next Steps:**
1. Run `python3 scripts/auto-deploy.py` to activate everything
2. Configure external service API keys
3. Set up Slack webhook for notifications
4. Monitor the [Actions tab](https://github.com/Trancendos/trancendos-ecosystem/actions) for deployment progress

**🔗 Quick Links:**
- [Repository](https://github.com/Trancendos/trancendos-ecosystem)
- [Actions Dashboard](https://github.com/Trancendos/trancendos-ecosystem/actions)
- [Security Overview](https://github.com/Trancendos/trancendos-ecosystem/security)
- [Deployments](https://github.com/Trancendos/trancendos-ecosystem/deployments)