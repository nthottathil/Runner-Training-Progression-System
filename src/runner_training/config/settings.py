"""Configuration settings for the application."""

from typing import Optional, Any
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator, ConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Model parameters
    target_mileage: float = Field(50.0, gt=0, description="Target weekly mileage")
    starting_mileage: float = Field(10.0, ge=0, description="Starting weekly mileage")
    a_parameter: float = Field(0.8, description="Model parameter a")
    b_parameter: float = Field(4.0, gt=0, description="Model parameter b")
    equation_choice: str = Field("exponential", description="Model type selection")
    
    # API settings
    api_host: str = Field("127.0.0.1", description="API host address")
    api_port: int = Field(8000, ge=1024, le=65535, description="API port")
    api_reload: bool = Field(True, description="Enable auto-reload for development")
    log_level: str = Field("info", description="Logging level")
    
    # Visualisation settings
    plot_weeks: int = Field(20, gt=0, description="Number of weeks to plot")
    plot_dpi: int = Field(100, gt=0, description="Plot resolution (DPI)")
    
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    @field_validator("equation_choice")
    @classmethod
    def validate_equation_choice(cls, v: str) -> str:
        """Validate equation choice."""
        valid_choices = ["exponential", "linear"]
        if v.lower() not in valid_choices:
            raise ValueError(f"Invalid equation choice. Must be one of: {valid_choices}")
        return v.lower()
    
    @field_validator("starting_mileage")
    @classmethod
    def validate_starting_less_than_target(cls, v: float, info) -> float:
        """Ensure starting mileage is less than target for exponential model."""
        values = info.data
        if "target_mileage" in values and "equation_choice" in values:
            if values["equation_choice"] == "exponential" and v >= values["target_mileage"]:
                raise ValueError("Starting mileage must be less than target for exponential model")
        return v


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()