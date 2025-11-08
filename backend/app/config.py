"""Application configuration and settings."""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
from supabase import create_client, Client


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
    
    # Supabase Configuration
    supabase_url: str = Field(
        default="",
        description="Supabase project URL"
    )
    supabase_anon_key: str = Field(
        default="",
        description="Supabase anonymous/public key"
    )
    supabase_service_role_key: str = Field(
        default="",
        description="Supabase service role key (for admin operations)"
    )
    
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


# Initialize Supabase client
def get_supabase_client() -> Optional[Client]:
    """Get Supabase client instance."""
    if settings.supabase_url and settings.supabase_anon_key:
        return create_client(settings.supabase_url, settings.supabase_anon_key)
    return None


def get_supabase_admin_client() -> Optional[Client]:
    """Get Supabase admin client with service role key."""
    if settings.supabase_url and settings.supabase_service_role_key:
        return create_client(settings.supabase_url, settings.supabase_service_role_key)
    return None


