"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import health, auth, preferences, scan


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Backend API for EatRite nutrition tracking app with food scanning and safety analysis",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix=settings.api_prefix, tags=["health"])
app.include_router(auth.router, prefix=settings.api_prefix, tags=["auth"])
app.include_router(preferences.router, prefix=settings.api_prefix, tags=["preferences"])
app.include_router(scan.router, prefix=settings.api_prefix, tags=["scan"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to EatRite API",
        "version": settings.version,
        "docs": "/docs",
        "endpoints": {
            "health": f"{settings.api_prefix}/health",
            "auth": {
                "register": f"{settings.api_prefix}/auth/register",
                "login": f"{settings.api_prefix}/auth/login",
                "me": f"{settings.api_prefix}/auth/me",
            },
            "preferences": f"{settings.api_prefix}/preferences",
            "scan": {
                "scan_image": f"{settings.api_prefix}/scan-image",
                "analyze": f"{settings.api_prefix}/analyze",
                "history": f"{settings.api_prefix}/scan-history",
            }
        }
    }


