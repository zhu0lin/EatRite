"""Application configuration and settings."""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    app_name: str = "EatRite API"
    version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    
    # Security
    secret_key: str = Field(
        default="your-secret-key-here-change-in-production",
        description="Secret key for JWT encoding/decoding"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS
    cors_origins: list[str] = [
        "http://localhost:8081",  # Expo default
        "http://localhost:19000", # Expo alternative
        "http://localhost:19006", # Expo web
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()


