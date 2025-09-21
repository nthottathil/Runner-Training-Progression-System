
"""Pydantic schemas for API requests and responses."""

from typing import Optional
from pydantic import BaseModel, Field, validator


class BaseRequest(BaseModel):
    """Base request with optional parameter overrides."""
    
    target_mileage: Optional[float] = Field(None, gt=0, description="Override target mileage")
    starting_mileage: Optional[float] = Field(None, ge=0, description="Override starting mileage")
    a_parameter: Optional[float] = Field(None, description="Override parameter a")
    b_parameter: Optional[float] = Field(None, gt=0, description="Override parameter b")


class MileageCalculationRequest(BaseRequest):
    """Request for calculating mileage at a specific week."""
    
    week_number: float = Field(..., ge=0, description="Week number (0-indexed)")


class WeekCalculationRequest(BaseRequest):
    """Request for calculating week for a specific mileage."""
    
    weekly_mileage: float = Field(..., ge=0, description="Target weekly mileage")


class RateOfChangeRequest(BaseRequest):
    """Request for calculating rate of change at a specific week."""
    
    week_number: float = Field(..., ge=0, description="Week number (0-indexed)")


class VisualisationRequest(BaseRequest):  
    """Request for generating visualisation data."""
    
    weeks_to_plot: int = Field(20, gt=0, le=52, description="Number of weeks to visualise")
    include_rate: bool = Field(True, description="Include rate of change plot")


class BaseResponse(BaseModel):
    """Base response with common fields."""
    
    equation_type: str = Field(..., description="Type of model used")
    parameters: dict = Field(..., description="Model parameters used")


class MileageCalculationResponse(BaseResponse):
    """Response for mileage calculation."""
    
    week_number: float = Field(..., description="Input week number")
    weekly_mileage: float = Field(..., description="Calculated weekly mileage")
    percentage_of_target: float = Field(..., description="Percentage of target mileage achieved")


class WeekCalculationResponse(BaseResponse):
    """Response for week calculation."""
    
    weekly_mileage: float = Field(..., description="Input weekly mileage")
    week_number: Optional[float] = Field(..., description="Calculated week number")
    is_achievable: bool = Field(..., description="Whether mileage is achievable")
    message: Optional[str] = Field(None, description="Additional information")


class RateOfChangeResponse(BaseResponse):
    """Response for rate of change calculation."""
    
    week_number: float = Field(..., description="Input week number")
    rate_of_change: float = Field(..., description="Rate of change (miles/week)")
    interpretation: str = Field(..., description="Human-readable interpretation")


class VisualisationResponse(BaseResponse):  
    """Response for visualisation data."""
    
    weeks: list[float] = Field(..., description="Week numbers")
    mileages: list[float] = Field(..., description="Weekly mileages")
    rates: Optional[list[float]] = Field(None, description="Rates of change")
    equation_latex: str = Field(..., description="LaTeX equation representation")
    plateau_week: Optional[float] = Field(None, description="Week when plateau is reached (linear model)")


class HealthCheckResponse(BaseModel):
    """Health check response."""
    
    status: str = Field("healthy", description="Service status")
    version: str = Field(..., description="API version")
    equation_type: str = Field(..., description="Current model type")
    default_parameters: dict = Field(..., description="Default model parameters")