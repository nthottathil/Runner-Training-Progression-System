#!/usr/bin/env python3
"""Script to run the API server."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import uvicorn
from src.runner_training.config.settings import Settings


def main():
    """Run the API server."""
    settings = Settings()
    
    print("Runner Training API Server")
    print("=" * 50)
    print(f"Model Type: {settings.equation_choice}")
    print(f"Target Mileage: {settings.target_mileage} miles")
    print(f"Starting Mileage: {settings.starting_mileage} miles")
    print(f"Parameters: a={settings.a_parameter}, b={settings.b_parameter}")
    print("=" * 50)
    print(f"Server: http://{settings.api_host}:{settings.api_port}")
    print(f"API Docs: http://{settings.api_host}:{settings.api_port}/docs")
    print(f"Auto-reload: {'Enabled' if settings.api_reload else 'Disabled'}")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    uvicorn.run(
        "src.runner_training.api.server:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload,
        log_level=settings.log_level
    )


if __name__ == "__main__":
    main()