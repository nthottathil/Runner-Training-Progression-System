"""API route handlers."""

from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from ..models.factory import ModelFactory
from ..config.settings import Settings, get_settings
from .schemas import (
    MileageCalculationRequest,
    MileageCalculationResponse,
    WeekCalculationRequest,
    WeekCalculationResponse,
    RateOfChangeRequest,
    RateOfChangeResponse,
    VisualisationRequest,
    VisualisationResponse,
    HealthCheckResponse
)

router = APIRouter(prefix="/api/v1", tags=["training"])


def get_model_params(request: dict, settings: Settings) -> dict:
    """Extract model parameters from request or use defaults."""
    return {
        "model_type": settings.equation_choice,
        "target_mileage": request.get("target_mileage") or settings.target_mileage,
        "starting_mileage": request.get("starting_mileage") or settings.starting_mileage,
        "a_parameter": request.get("a_parameter") or settings.a_parameter,
        "b_parameter": request.get("b_parameter") or settings.b_parameter
    }


@router.post("/calculate-mileage", response_model=MileageCalculationResponse)
async def calculate_mileage(
    request: MileageCalculationRequest, 
    settings: Settings = Depends(get_settings)
):
    """Calculate weekly mileage for a given week."""
    try:
        params = get_model_params(request.dict(), settings)
        model = ModelFactory.create(**params)
        
        mileage = model.calculate_mileage(request.week_number)
        percentage = (mileage / params["target_mileage"]) * 100
        
        return MileageCalculationResponse(
            week_number=request.week_number,
            weekly_mileage=round(mileage, 2),
            percentage_of_target=round(percentage, 1),
            equation_type=model.model_type,
            parameters=params
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/calculate-week", response_model=WeekCalculationResponse)
async def calculate_week(
    request: WeekCalculationRequest, 
    settings: Settings = Depends(get_settings)
):
    """Calculate week number for a given mileage."""
    try:
        params = get_model_params(request.dict(), settings)
        model = ModelFactory.create(**params)
        
        week = model.calculate_week(request.weekly_mileage)
        
        if week is None:
            return WeekCalculationResponse(
                weekly_mileage=request.weekly_mileage,
                week_number=None,
                is_achievable=False,
                message=f"Mileage {request.weekly_mileage} is outside valid range",
                equation_type=model.model_type,
                parameters=params
            )
        
        message = None
        if week == float('inf'):
            message = "Target mileage is approached asymptotically (never fully reached)"
        
        return WeekCalculationResponse(
            weekly_mileage=request.weekly_mileage,
            week_number=round(week, 2) if week != float('inf') else None,
            is_achievable=True,
            message=message,
            equation_type=model.model_type,
            parameters=params
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/rate-of-change", response_model=RateOfChangeResponse)
async def calculate_rate(
    request: RateOfChangeRequest, 
    settings: Settings = Depends(get_settings)
):
    """Calculate rate of change at a given week."""
    try:
        params = get_model_params(request.dict(), settings)
        model = ModelFactory.create(**params)
        
        rate = model.calculate_rate_of_change(request.week_number)
        
        interpretation = f"At week {request.week_number}, mileage "
        if abs(rate) < 0.01:
            interpretation += "is stable (plateau reached)"
        elif rate > 0:
            interpretation += f"increases by {abs(rate):.3f} miles per week"
        else:
            interpretation += f"decreases by {abs(rate):.3f} miles per week"
        
        return RateOfChangeResponse(
            week_number=request.week_number,
            rate_of_change=round(rate, 4),
            interpretation=interpretation,
            equation_type=model.model_type,
            parameters=params
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/visualise", response_model=VisualisationResponse)
async def get_visualisation_data(
    request: VisualisationRequest,
    settings: Settings = Depends(get_settings)
):
    """Get data for visualisation."""
    try:
        params = get_model_params(request.dict(), settings)
        model = ModelFactory.create(**params)
        
        weeks = list(range(request.weeks_to_plot))
        mileages = [model.calculate_mileage(w) for w in weeks]
        rates = None
        
        if request.include_rate:
            rates = [model.calculate_rate_of_change(w) for w in weeks]
        
        plateau_week = None
        if model.model_type == "linear":
            from ..models.linear import LinearModel
            if isinstance(model, LinearModel):
                plateau_week = model._get_plateau_week()
        
        return VisualisationResponse(
            weeks=weeks,
            mileages=[round(m, 2) for m in mileages],
            rates=[round(r, 4) for r in rates] if rates else None,
            equation_latex=model.get_equation_latex(),
            plateau_week=round(plateau_week, 2) if plateau_week else None,
            equation_type=model.model_type,
            parameters=params
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/health", response_model=HealthCheckResponse)
async def health_check(settings: Settings = Depends(get_settings)):
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        version="2.0.0",
        equation_type=settings.equation_choice,
        default_parameters={
            "target_mileage": settings.target_mileage,
            "starting_mileage": settings.starting_mileage,
            "a_parameter": settings.a_parameter,
            "b_parameter": settings.b_parameter
        }
    )