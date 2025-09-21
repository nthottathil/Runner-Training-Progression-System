"""Factory for creating training models."""

from typing import Union, Literal
from .base import BaseTrainingModel, ModelParameters
from .exponential import ExponentialModel
from .linear import LinearModel

ModelType = Literal["exponential", "linear"]


class ModelFactory:
    """Factory class for creating training models."""
    
    _models = {
        "exponential": ExponentialModel,
        "linear": LinearModel
    }
    
    @classmethod
    def create(
        cls,
        model_type: str,
        target_mileage: float,
        starting_mileage: float,
        a_parameter: float,
        b_parameter: float
    ) -> BaseTrainingModel:
        """
        Create a training model instance.
        
        Args:
            model_type: Type of model ("exponential" or "linear")
            target_mileage: Target weekly mileage
            starting_mileage: Starting weekly mileage
            a_parameter: Model-specific parameter a
            b_parameter: Model-specific parameter b
            
        Returns:
            Instance of the specified training model
            
        Raises:
            ValueError: If model_type is not recognized
        """
        model_type_lower = model_type.lower()
        
        if model_type_lower not in cls._models:
            available = ", ".join(cls._models.keys())
            raise ValueError(
                f"Unknown model type: {model_type}. Available: {available}"
            )
        
        params = ModelParameters(
            target_mileage=target_mileage,
            starting_mileage=starting_mileage,
            a_parameter=a_parameter,
            b_parameter=b_parameter
        )
        
        model_class = cls._models[model_type_lower]
        return model_class(params)
    
    @classmethod
    def available_models(cls) -> list[str]:
        """Get list of available model types."""
        return list(cls._models.keys())