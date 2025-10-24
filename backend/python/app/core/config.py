from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Represents the application's configuration settings.

    Attributes:
        ENVIRONMENT (str): The application's runtime environment (e.g., "development", "production").
        DEBUG (bool): A flag indicating whether debug mode is enabled.
        DATABASE_URL (str): The connection URL for the primary database.
        REDIS_URL (str): The connection URL for Redis.
        SECRET_KEY (str): The secret key for cryptographic operations.
        ALGORITHM (str): The algorithm used for token signing.
        ACCESS_TOKEN_EXPIRE_MINUTES (int): The expiration time for access tokens in minutes.
        CORS_ALLOWED_ORIGINS (List[str]): A list of allowed origins for Cross-Origin Resource Sharing (CORS).
        ALLOWED_HOSTS (List[str]): A list of allowed hostnames.
        ML_MODEL_PATH (str): The file path to the machine learning models.
        TF_SERVING_URL (str): The URL for the TensorFlow Serving instance.
        PLAID_CLIENT_ID (str): The client ID for the Plaid API.
        PLAID_SECRET (str): The secret key for the Plaid API.
        PLAID_ENVIRONMENT (str): The environment for the Plaid API (e.g., "sandbox", "development", "production").
        CELERY_BROKER_URL (str): The connection URL for the Celery message broker.
        CELERY_RESULT_BACKEND (str): The connection URL for the Celery result backend.
    """
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://trancendos:password@localhost:5432/trancendos_ai")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://trancendos.com"
    ]
    
    # Allowed hosts
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "*.trancendos.com"]
    
    # AI Model Configuration
    ML_MODEL_PATH: str = os.getenv("ML_MODEL_PATH", "./models")
    TF_SERVING_URL: str = os.getenv("TF_SERVING_URL", "http://localhost:8501")
    
    # External APIs
    PLAID_CLIENT_ID: str = os.getenv("PLAID_CLIENT_ID", "")
    PLAID_SECRET: str = os.getenv("PLAID_SECRET", "")
    PLAID_ENVIRONMENT: str = os.getenv("PLAID_ENVIRONMENT", "sandbox")
    
    # Celery
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    class Config:
        env_file = ".env"
        case_sensitive = True

def get_settings() -> Settings:
    """Returns the application's configuration settings.

    Returns:
        Settings: An instance of the Settings class.
    """
    return Settings()