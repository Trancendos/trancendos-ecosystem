#!/bin/bash

# Trancendos Ecosystem - GitHub Actions Enablement Script
# Enables workflows, sets up repository configuration, and initializes automation

set -e

echo "🚀 Trancendos Ecosystem - GitHub Actions Setup"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check dependencies
check_dependencies() {
    echo -e "${BLUE}Checking dependencies...${NC}"
    
    # Check if gh CLI is installed
    if ! command -v gh &> /dev/null; then
        echo -e "${RED}❌ GitHub CLI (gh) is not installed${NC}"
        echo "Please install it from: https://cli.github.com/"
        exit 1
    fi
    
    # Check if user is authenticated
    if ! gh auth status &> /dev/null; then
        echo -e "${RED}❌ GitHub CLI not authenticated${NC}"
        echo "Please run: gh auth login"
        exit 1
    fi
    
    # Check if we're in the right repository
    repo_info=$(gh repo view --json owner,name 2>/dev/null || echo "{}")
    if [[ "$repo_info" == "{}" ]]; then
        echo -e "${RED}❌ Not in a GitHub repository directory${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ All dependencies satisfied${NC}"
}

# Enable GitHub Actions
enable_actions() {
    echo -e "${BLUE}Enabling GitHub Actions...${NC}"
    
    # Enable Actions for the repository
    gh api \
        --method PUT \
        -H "Accept: application/vnd.github+json" \
        "/repos/{owner}/{repo}/actions/permissions" \
        -f enabled=true \
        -f allowed_actions=all
    
    echo -e "${GREEN}✅ GitHub Actions enabled${NC}"
}

# Set up repository secrets
setup_secrets() {
    echo -e "${BLUE}Setting up repository secrets...${NC}"
    
    # Generate initial secrets if they don't exist
    if [[ -f "scripts/generate-secrets.py" ]]; then
        echo "🔐 Generating initial secrets..."
        python3 scripts/generate-secrets.py --env staging --output .env.staging
        
        # Read secrets from generated file and set them in GitHub
        while IFS='=' read -r key value; do
            # Skip comments and empty lines
            if [[ "$key" =~ ^#.*$ ]] || [[ -z "$key" ]]; then
                continue
            fi
            
            # Remove any quotes from the value
            value=$(echo "$value" | sed 's/^"//;s/"$//')
            
            # Set the secret (only if it contains actual generated content)
            if [[ "$value" != *"your_"*"_here" ]] && [[ -n "$value" ]]; then
                echo "Setting secret: $key"
                echo "$value" | gh secret set "$key" --body-file -
            fi
        done < .env.staging
        
        echo -e "${GREEN}✅ Repository secrets configured${NC}"
    else
        echo -e "${YELLOW}⚠️ Secret generation script not found, skipping...${NC}"
    fi
}

# Configure repository settings
configure_repository() {
    echo -e "${BLUE}Configuring repository settings...${NC}"
    
    # Enable vulnerability alerts
    gh api \
        --method PUT \
        -H "Accept: application/vnd.github+json" \
        "/repos/{owner}/{repo}/vulnerability-alerts"
    
    # Enable automated security fixes
    gh api \
        --method PUT \
        -H "Accept: application/vnd.github+json" \
        "/repos/{owner}/{repo}/automated-security-fixes"
    
    # Configure branch protection (if main branch exists)
    if gh api "/repos/{owner}/{repo}/branches/main" &> /dev/null; then
        gh api \
            --method PUT \
            -H "Accept: application/vnd.github+json" \
            "/repos/{owner}/{repo}/branches/main/protection" \
            -f required_status_checks='{"strict":true,"contexts":["build-and-test"]}' \
            -f enforce_admins=false \
            -f required_pull_request_reviews='{"required_approving_review_count":1}' \
            -f restrictions=null \
            -f allow_force_pushes=false \
            -f allow_deletions=false
        
        echo -e "${GREEN}✅ Branch protection configured${NC}"
    fi
    
    echo -e "${GREEN}✅ Repository settings configured${NC}"
}

# Set up environments
setup_environments() {
    echo -e "${BLUE}Setting up deployment environments...${NC}"
    
    # Create staging environment
    gh api \
        --method PUT \
        -H "Accept: application/vnd.github+json" \
        "/repos/{owner}/{repo}/environments/staging" \
        -f wait_timer=0 \
        -f reviewers='[]' \
        -f deployment_branch_policy='{"protected_branches":false,"custom_branch_policies":true}' || true
    
    # Create production environment with protection
    gh api \
        --method PUT \
        -H "Accept: application/vnd.github+json" \
        "/repos/{owner}/{repo}/environments/production" \
        -f wait_timer=300 \
        -f reviewers='[]' \
        -f deployment_branch_policy='{"protected_branches":true,"custom_branch_policies":false}' || true
    
    echo -e "${GREEN}✅ Deployment environments created${NC}"
}

# Enable workflows
enable_workflows() {
    echo -e "${BLUE}Enabling workflows...${NC}"
    
    # Get list of workflow files
    workflow_files=$(find .github/workflows -name "*.yml" -o -name "*.yaml" 2>/dev/null || echo "")
    
    if [[ -n "$workflow_files" ]]; then
        echo "Found workflow files:"
        echo "$workflow_files"
        
        # Enable each workflow
        for workflow_file in $workflow_files; do
            workflow_name=$(basename "$workflow_file")
            echo "📋 Enabling workflow: $workflow_name"
            
            # Workflows are enabled by default when they exist in the repository
            # We just need to ensure Actions are enabled (done above)
        done
        
        echo -e "${GREEN}✅ Workflows enabled${NC}"
    else
        echo -e "${YELLOW}⚠️ No workflow files found${NC}"
    fi
}

# Trigger initial workflow run
trigger_workflows() {
    echo -e "${BLUE}Triggering initial workflow runs...${NC}"
    
    # Trigger the main deployment workflow if it exists
    if [[ -f ".github/workflows/ecosystem-deploy.yml" ]]; then
        echo "🚀 Triggering ecosystem deployment workflow..."
        gh workflow run ecosystem-deploy.yml \
            --ref main \
            -f environment=staging \
            -f services=all || echo "Note: Workflow trigger may require workflows to be committed first"
    fi
    
    # Trigger service orchestration workflow if it exists
    if [[ -f ".github/workflows/service-orchestration.yml" ]]; then
        echo "🎼 Triggering service orchestration workflow..."
        gh workflow run service-orchestration.yml \
            --ref main \
            -f action=health-check \
            -f target_environment=staging || echo "Note: Workflow trigger may require workflows to be committed first"
    fi
    
    echo -e "${GREEN}✅ Initial workflows triggered${NC}"
}

# Setup monitoring and notifications
setup_monitoring() {
    echo -e "${BLUE}Setting up monitoring...${NC}"
    
    # Create issue templates if they don't exist
    mkdir -p .github/ISSUE_TEMPLATE
    
    # Bug report template
    cat > .github/ISSUE_TEMPLATE/bug_report.yml << 'EOF'
name: 🐛 Bug Report
description: Report a bug in the Trancendos Ecosystem
title: "[BUG] "
labels: ["bug", "needs-triage"]
assignees: []

body:
  - type: markdown
    attributes:
      value: |
        Thanks for taking the time to fill out this bug report!

  - type: textarea
    id: what-happened
    attributes:
      label: What happened?
      description: A clear and concise description of what the bug is.
      placeholder: Tell us what went wrong!
    validations:
      required: true

  - type: dropdown
    id: environment
    attributes:
      label: Environment
      description: Which environment did this occur in?
      options:
        - Development
        - Staging  
        - Production
    validations:
      required: true

  - type: textarea
    id: logs
    attributes:
      label: Relevant log output
      description: Please copy and paste any relevant log output.
      render: shell
EOF

    # Feature request template
    cat > .github/ISSUE_TEMPLATE/feature_request.yml << 'EOF'
name: ✨ Feature Request
description: Suggest a new feature for the Trancendos Ecosystem
title: "[FEATURE] "
labels: ["enhancement", "needs-triage"]

body:
  - type: textarea
    id: feature-description
    attributes:
      label: Feature Description
      description: A clear and concise description of the feature you'd like to see.
      placeholder: Describe the feature...
    validations:
      required: true

  - type: textarea
    id: use-case
    attributes:
      label: Use Case
      description: Describe the use case and why this feature would be valuable.
      placeholder: How would this feature be used?
    validations:
      required: true
EOF

    echo -e "${GREEN}✅ Monitoring and templates configured${NC}"
}

# Main execution
main() {
    echo -e "${YELLOW}Starting GitHub Actions setup for Trancendos Ecosystem...${NC}"
    echo ""
    
    check_dependencies
    echo ""
    
    enable_actions
    echo ""
    
    setup_secrets  
    echo ""
    
    configure_repository
    echo ""
    
    setup_environments
    echo ""
    
    enable_workflows
    echo ""
    
    setup_monitoring
    echo ""
    
    trigger_workflows
    echo ""
    
    echo -e "${GREEN}🎉 GitHub Actions setup complete!${NC}"
    echo ""
    echo -e "${BLUE}Next steps:${NC}"
    echo "1. Check the Actions tab to see workflow runs"
    echo "2. Configure external service API keys in repository secrets"
    echo "3. Review and customize workflow triggers as needed"
    echo "4. Monitor the first deployment in the Actions tab"
    echo ""
    echo -e "${YELLOW}Repository: $(gh repo view --json url -q .url)${NC}"
    echo -e "${YELLOW}Actions: $(gh repo view --json url -q .url)/actions${NC}"
}

# Handle script arguments
case "${1:-setup}" in
    "setup"|"")
        main
        ;;
    "secrets-only")
        setup_secrets
        ;;
    "enable-only") 
        enable_actions
        enable_workflows
        ;;
    "monitor-only")
        setup_monitoring
        ;;
    "help"|"-h"|"--help")
        echo "Usage: $0 [setup|secrets-only|enable-only|monitor-only|help]"
        echo ""
        echo "Commands:"
        echo "  setup         - Full setup (default)"
        echo "  secrets-only  - Only generate and set secrets"
        echo "  enable-only   - Only enable Actions and workflows"
        echo "  monitor-only  - Only setup monitoring templates"
        echo "  help          - Show this help"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Run '$0 help' for usage information"
        exit 1
        ;;
esac