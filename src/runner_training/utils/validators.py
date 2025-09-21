"""Validation utilities for the application."""

from typing import Any, Dict, Optional


class ParameterValidator:
    """Validator for model parameters."""
    
    @staticmethod
    def validate_mileage_range(
        starting: float,
        target: float,
        model_type: str
    ) -> None:
        """
        Validate mileage range for a given model type.
        
        Args:
            starting: Starting mileage
            target: Target mileage
            model_type: Type of model
            
        Raises:
            ValueError: If validation fails
        """
        if target <= 0:
            raise ValueError(f"Target mileage must be positive, got {target}")
        
        if starting < 0:
            raise ValueError(f"Starting mileage must be non-negative, got {starting}")
        
        if model_type == "exponential" and starting >= target:
            raise ValueError(
                f"For exponential model, starting ({starting}) must be less than target ({target})"
            )
        
        if model_type == "linear" and starting > target:
            raise ValueError(
                f"For linear model, starting ({starting}) cannot exceed target ({target})"
            )
    
    @staticmethod
    def validate_model_parameters(
        a_param: float,
        b_param: float,
        model_type: str
    ) -> None:
        """
        Validate model-specific parameters.
        
        Args:
            a_param: Parameter a
            b_param: Parameter b
            model_type: Type of model
            
        Raises:
            ValueError: If validation fails
        """
        if b_param <= 0:
            raise ValueError(f"Parameter b must be positive, got {b_param}")
        
        if model_type == "exponential":
            if not 0 < a_param < 1:
                raise ValueError(
                    f"For exponential model, parameter a must be in (0, 1), got {a_param}"
                )
        elif model_type == "linear":
            if a_param <= 0:
                raise ValueError(
                    f"For linear model, parameter a must be positive, got {a_param}"
                )
    
    @staticmethod
    def validate_week_number(week: float) -> None:
        """
        Validate week number.
        
        Args:
            week: Week number to validate
            
        Raises:
            ValueError: If week is negative
        """
        if week < 0:
            raise ValueError(f"Week number must be non-negative, got {week}")


class DataValidator:
    """Validator for data consistency."""
    
    @staticmethod
    def validate_request_parameters(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean request parameters.
        
        Args:
            params: Request parameters
            
        Returns:
            Cleaned parameters
            
        Raises:
            ValueError: If validation fails
        """
        cleaned = {}
        
        for key, value in params.items():
            if value is not None:
                if key in ["target_mileage", "starting_mileage", "a_parameter", "b_parameter"]:
                    if not isinstance(value, (int, float)):
                        raise ValueError(f"{key} must be numeric, got {type(value).__name__}")
                cleaned[key] = value
        
        return cleaned