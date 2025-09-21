"""Pytest configuration and shared fixtures."""

import pytest
import sys
import os
from typing import Generator
from fastapi.testclient import TestClient

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.runner_training.config.settings import Settings
from src.runner_training.models.factory import ModelFactory
from src.runner_training.models.base import ModelParameters


@pytest.fixture
def test_settings() -> Settings:
    """Create test settings."""
    return Settings(
        target_mileage=50.0,
        starting_mileage=10.0,
        a_parameter=0.8,
        b_parameter=4.0,
        equation_choice="exponential"
    )


@pytest.fixture
def exponential_params() -> ModelParameters:
    """Create exponential model parameters."""
    return ModelParameters(
        target_mileage=50.0,
        starting_mileage=10.0,
        a_parameter=0.8,
        b_parameter=4.0
    )


@pytest.fixture
def linear_params() -> ModelParameters:
    """Create linear model parameters."""
    return ModelParameters(
        target_mileage=50.0,
        starting_mileage=10.0,
        a_parameter=2.0,
        b_parameter=1.0
    )


@pytest.fixture
def test_client(test_settings: Settings) -> Generator[TestClient, None, None]:
    """Create test client for API."""
    from src.runner_training.api.server import create_app
    
    app = create_app(test_settings)
    with TestClient(app) as client:
        yield client


@pytest.fixture
def model_factory() -> ModelFactory:
    """Create model factory instance."""
    return ModelFactory()