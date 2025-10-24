from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import structlog
import uvicorn
from prometheus_client import make_asgi_app, Counter, Histogram, Gauge

from app.core.config import get_settings
from app.core.database import create_tables
from app.api.v1.router import api_router
from app.core.security import verify_token
from app.core.logging import setup_logging

# Setup logging
setup_logging()
logger = structlog.get_logger()

# Metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Active connections')

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Luminous-MastermindAI service")
    await create_tables()
    yield
    # Shutdown
    logger.info("Shutting down Luminous-MastermindAI service")

app = FastAPI(
    title="Luminous-MastermindAI",
    description="AI-powered analytics and decision support system for Trancendos Ecosystem",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/api/redoc" if settings.ENVIRONMENT != "production" else None,
)

# Security
security = HTTPBearer()

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.get("/")
async def root():
    return {
        "service": "Luminous-MastermindAI",
        "version": "1.0.0",
        "status": "running",
        "description": "AI-powered analytics and decision support system"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "luminous-mastermind-ai",
        "version": "1.0.0"
    }

# Dependency for authentication
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = verify_token(token)
        return payload
    except Exception as e:
        logger.error("Authentication failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.ENVIRONMENT == "development",
        log_config=None  # Use structlog instead
    )