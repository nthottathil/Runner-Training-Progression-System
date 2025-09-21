"""FastAPI application server."""

from typing import Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router
from ..config.settings import Settings


def create_app(settings: Optional[Settings] = None) -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Args:
        settings: Application settings
        
    Returns:
        Configured FastAPI application
    """
    if settings is None:
        settings = Settings()
    
    app = FastAPI(
        title="Runner Training API",
        description="Advanced training progression calculator with multiple models",
        version="2.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routes
    app.include_router(router)
    
    # Store settings in app state
    app.state.settings = settings
    
    @app.get("/")
    async def root():
        """Root endpoint."""
        return {
            "message": "Runner Training API v2.0",
            "documentation": "/docs",
            "health": "/api/v1/health"
        }
    
    return app

app = create_app()