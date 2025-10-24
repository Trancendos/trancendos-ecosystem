# 🛡️ Docker & Network Hardening Guide - IMMEDIATE IMPLEMENTATION

**Priority:** 🚨 CRITICAL - Apply within 24 hours  
**Target:** Resolve 30+ security vulnerabilities  
**Compliance:** PCI DSS requirements  

## 🎯 Phase 1: IMMEDIATE Docker Hardening (2-4 hours)

### 1. Remove Exposed Database Ports 🚫

**CRITICAL FIX:** Remove external port exposure for internal services

```yaml
# ❌ VULNERABLE - Current configuration
postgres:
  ports:
    - "5432:5432"  # EXPOSED TO PUBLIC
redis:
  ports:
    - "6379:6379"  # EXPOSED TO PUBLIC

# ✅ SECURE - Internal access only
postgres:
  # No external ports - internal network only
  expose:
    - "5432"
redis:
  # No external ports - internal network only  
  expose:
    - "6379"
```

### 2. Container Security Hardening 🔒

**Create non-root users for all containers:**

```dockerfile
# ✅ SECURE Dockerfile pattern
FROM openjdk:21-jre-slim

# Create non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set security options
USER appuser:appuser
WORKDIR /app

# Read-only root filesystem
# Use in docker-compose with: read_only: true
```

### 3. Network Segmentation Implementation 🌐

**Create isolated networks for different tiers:**

```yaml
# ✅ SECURE Network Architecture
networks:
  # Frontend tier - DMZ
  frontend-network:
    driver: bridge
    internal: false
  
  # Application tier - Internal only
  backend-network:
    driver: bridge
    internal: true
  
  # Database tier - Highly restricted
  database-network:
    driver: bridge
    internal: true
  
  # Monitoring tier - Separate access
  monitoring-network:
    driver: bridge
    internal: false
```

### 4. Resource Limits & Security Constraints 📊

```yaml
# ✅ Add to ALL services
security_opt:
  - no-new-privileges:true
  - apparmor:docker-default
  - seccomp:unconfined
read_only: true
tmpfs:
  - /tmp
  - /run
deploy:
  resources:
    limits:
      memory: 512M
      cpus: '0.5'
    reservations:
      memory: 256M
      cpus: '0.25'
```

## 🔧 Phase 2: Immediate Docker Compose Fixes

### Secure PostgreSQL Configuration

```yaml
postgres:
  image: postgres:15-alpine
  environment:
    POSTGRES_DB: trancendos
    POSTGRES_USER: trancendos
    POSTGRES_PASSWORD_FILE: /run/secrets/postgres_password
  secrets:
    - postgres_password
  volumes:
    - postgres_data:/var/lib/postgresql/data:Z
    - ./database/init:/docker-entrypoint-initdb.d:ro
  networks:
    - database-network
  security_opt:
    - no-new-privileges:true
  read_only: true
  tmpfs:
    - /tmp
    - /run
  deploy:
    resources:
      limits:
        memory: 1G
        cpus: '1.0'
```

### Secure Redis Configuration

```yaml
redis:
  image: redis:7-alpine
  command: >
    redis-server
    --requirepass "$${REDIS_PASSWORD}"
    --appendonly yes
    --save 60 1
  environment:
    REDIS_PASSWORD_FILE: /run/secrets/redis_password
  secrets:
    - redis_password
  volumes:
    - redis_data:/data:Z
  networks:
    - database-network
  security_opt:
    - no-new-privileges:true
  read_only: true
  tmpfs:
    - /tmp
```

### Secure Nginx Configuration

```yaml
nginx:
  image: nginx:alpine
  ports:
    - "443:443"
    # ❌ REMOVE: - "80:80"  # HTTP DISABLED
  volumes:
    - ./nginx/nginx-secure.conf:/etc/nginx/nginx.conf:ro
    - ./ssl:/etc/ssl/certs:ro
  networks:
    - frontend-network
    - backend-network
  security_opt:
    - no-new-privileges:true
  read_only: true
  tmpfs:
    - /var/cache/nginx
    - /var/run
  depends_on:
    - frontend
    - backend-java
    - backend-python
```

## 🔐 Phase 3: Secrets Management Implementation

### Docker Secrets Configuration

```yaml
secrets:
  postgres_password:
    file: ./secrets/postgres_password.txt
  redis_password:
    file: ./secrets/redis_password.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt
  encryption_key:
    file: ./secrets/encryption_key.txt
  stripe_api_key:
    external: true
  plaid_secret:
    external: true
```

### Environment Variable Security

```yaml
# ✅ SECURE - Use secrets instead of env vars
environment:
  - SPRING_PROFILES_ACTIVE=production
  - DATABASE_URL=postgresql://trancendos@postgres:5432/trancendos
  - REDIS_URL=redis://redis:6379
  # ❌ REMOVE ALL HARDCODED SECRETS
```

## 🌐 Network Security Implementation

### Firewall Rules (iptables)

```bash
#!/bin/bash
# Docker Host Firewall Rules

# Flush existing rules
iptables -F
iptables -X

# Default policies
iptables -P INPUT DROP
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# SSH access (change port from 22)
iptables -A INPUT -p tcp --dport 2222 -j ACCEPT

# HTTPS only
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Block direct database access
iptables -A INPUT -p tcp --dport 5432 -j DROP
iptables -A INPUT -p tcp --dport 6379 -j DROP

# Save rules
iptables-save > /etc/iptables/rules.v4
```

### Container Network Policies

```yaml
# Network isolation rules
services:
  frontend:
    networks:
      - frontend-network
    # Cannot access database directly
  
  backend-java:
    networks:
      - backend-network
      - database-network
    # Can access database
  
  postgres:
    networks:
      - database-network
    # Isolated from frontend
```

## 🔍 Security Monitoring Setup

### Container Security Scanning

```yaml
# Add to CI/CD pipeline
- name: Container Security Scan
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'ghcr.io/trancendos/trancendos-ecosystem:latest'
    format: 'sarif'
    output: 'trivy-results.sarif'
    
- name: Upload Trivy scan results
  uses: github/codeql-action/upload-sarif@v2
  with:
    sarif_file: 'trivy-results.sarif'
```

### Runtime Security Monitoring

```yaml
# Add security monitoring sidecar
security-monitor:
  image: falcosecurity/falco:latest
  privileged: true
  volumes:
    - /var/run/docker.sock:/host/var/run/docker.sock:ro
    - /dev:/host/dev:ro
    - /proc:/host/proc:ro
    - /boot:/host/boot:ro
    - /lib/modules:/host/lib/modules:ro
    - /usr:/host/usr:ro
  command:
    - /usr/bin/falco
    - --modern-bpf
```

## 🚦 Implementation Checklist

### Immediate Actions (Next 4 Hours)

- [ ] **Remove exposed database ports** (5432, 6379)
- [ ] **Implement network segmentation** (3 isolated networks)
- [ ] **Add container security constraints** (no-new-privileges, read-only)
- [ ] **Create non-root users** in all Dockerfiles
- [ ] **Disable HTTP port 80** (HTTPS only)

### Security Hardening (Next 24 Hours)

- [ ] **Implement Docker secrets** for all sensitive data
- [ ] **Add resource limits** to prevent DoS attacks
- [ ] **Configure container security profiles** (AppArmor/SELinux)
- [ ] **Set up security monitoring** (Falco/Trivy)
- [ ] **Implement firewall rules** (iptables/ufw)

### Compliance Validation (Next 48 Hours)

- [ ] **PCI DSS network segmentation** verification
- [ ] **Audit logging configuration** for all containers
- [ ] **Access control validation** (RBAC implementation)
- [ ] **Encryption verification** (data at rest/transit)
- [ ] **Security scanning integration** in CI/CD

## ⚠️ CRITICAL WARNINGS

### Before Implementation

1. **Backup Current Configuration** - Save current docker-compose.yml
2. **Test in Staging First** - Never apply directly to production
3. **Plan Downtime** - Some changes require service restart
4. **Verify Dependencies** - Ensure all services can communicate through new networks

### After Implementation

1. **Validate Connectivity** - Test all service interactions
2. **Monitor Logs** - Watch for connection errors or access denials  
3. **Performance Check** - Verify resource limits don't impact performance
4. **Security Scan** - Run vulnerability assessment to confirm fixes

## 🆘 Emergency Rollback Plan

If hardening breaks functionality:

```bash
# Quick rollback steps
1. git checkout HEAD~1 docker-compose.yml
2. docker-compose down
3. docker-compose up -d
4. Monitor service health
5. Investigate specific failure point
```

---

**Next Steps:** After implementing these hardening measures, proceed with PCI DSS compliance validation and security audit verification.

**Support:** For implementation assistance, create GitHub issue with specific hardening questions.