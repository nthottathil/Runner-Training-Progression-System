"""Base abstract class for all training models."""

from abc import ABC, abstractmethod
from typing import Optional
from dataclasses import dataclass


@dataclass
class ModelParameters:
    """Parameters for training models."""
    target_mileage: float
    starting_mileage: float
    a_parameter: float
    b_parameter: float

    def __post_init__(self) -> None:
        """Validate parameters after initialisation."""
        if self.target_mileage <= 0:
            raise ValueError("Target mileage must be positive")
        if self.starting_mileage < 0:
            raise ValueError("Starting mileage must be non-negative")


class BaseTrainingModel(ABC):
    """Abstract base class for training progression models."""
    
    def __init__(self, params: ModelParameters) -> None:
        """
        Initialize the training model.
        
        Args:
            params: Model parameters including target and starting mileage
        """
        self.params = params
        self._validate_parameters()
    
    @abstractmethod
    def _validate_parameters(self) -> None:
        """Validate model-specific parameter constraints."""
        pass
    
    @abstractmethod
    def calculate_mileage(self, week: float) -> float:
        """
        Calculate weekly mileage for a given week.
        
        Args:
            week: Week number (0-indexed)
            
        Returns:
            Weekly mileage for the specified week
        """
        pass
    
    @abstractmethod
    def calculate_week(self, mileage: float) -> Optional[float]:
        """
        Calculate week number for a given mileage.
        
        Args:
            mileage: Target weekly mileage
            
        Returns:
            Week number when mileage is achieved, or None if invalid
        """
        pass
    
    @abstractmethod
    def calculate_rate_of_change(self, week: float) -> float:
        """
        Calculate the rate of change at a given week.
        
        Args:
            week: Week number
            
        Returns:
            Rate of change (derivative) at the specified week
        """
        pass
    
    @property
    @abstractmethod
    def model_type(self) -> str:
        """Return the model type identifier."""
        pass
    
    def get_equation_latex(self) -> str:
        """
        Get LaTeX representation of the model equation.
        
        Returns:
            LaTeX string for the equation
        """
        return ""