"""Exponential training progression model."""

import math
from typing import Optional
from .base import BaseTrainingModel, ModelParameters


class ExponentialModel(BaseTrainingModel):
    """
    Exponential progression model.
    
    Equation: M(n) = T - (T - S) * a^(n/b)
    where:
        M(n) = mileage at week n
        T = target mileage
        S = starting mileage
        a = decay parameter (0 < a < 1)
        b = time scale parameter
    """
    
    def _validate_parameters(self) -> None:
        """Validate exponential model specific constraints."""
        if not 0 < self.params.a_parameter < 1:
            raise ValueError(
                f"Parameter 'a' must be in (0, 1), got {self.params.a_parameter}"
            )
        if self.params.b_parameter <= 0:
            raise ValueError(
                f"Parameter 'b' must be positive, got {self.params.b_parameter}"
            )
        if self.params.starting_mileage >= self.params.target_mileage:
            raise ValueError(
                "Starting mileage must be less than target mileage for exponential model"
            )
    
    def calculate_mileage(self, week: float) -> float:
        """Calculate mileage using exponential progression."""
        if week < 0:
            raise ValueError(f"Week must be non-negative, got {week}")
        
        T = self.params.target_mileage
        S = self.params.starting_mileage
        a = self.params.a_parameter
        b = self.params.b_parameter
        
        decay_factor = a ** (week / b)
        return T - (T - S) * decay_factor
    
    def calculate_week(self, mileage: float) -> Optional[float]:
        """Calculate week for given mileage using inverse exponential."""
        S = self.params.starting_mileage
        T = self.params.target_mileage
        
        if not S <= mileage <= T:
            return None
        
        if mileage == T:
            return float('inf')
        
        a = self.params.a_parameter
        b = self.params.b_parameter
        
        ratio = (T - mileage) / (T - S)
        if ratio <= 0:
            return None
        
        week = b * math.log(ratio) / math.log(a)
        return max(0.0, week)
    
    def calculate_rate_of_change(self, week: float) -> float:
        """Calculate derivative of exponential function."""
        if week < 0:
            raise ValueError(f"Week must be non-negative, got {week}")
        
        T = self.params.target_mileage
        S = self.params.starting_mileage
        a = self.params.a_parameter
        b = self.params.b_parameter
        
        coefficient = -(T - S) / b
        exponential = a ** (week / b)
        log_a = math.log(a)
        
        return coefficient * exponential * log_a
    
    @property
    def model_type(self) -> str:
        """Return model type identifier."""
        return "exponential"
    
    def get_equation_latex(self) -> str:
        """Get LaTeX representation of exponential equation."""
        return r"M(n) = T - (T - S) \cdot a^{n/b}"