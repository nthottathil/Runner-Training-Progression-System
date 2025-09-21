"""Linear training progression model."""

from typing import Optional
from .base import BaseTrainingModel, ModelParameters


class LinearModel(BaseTrainingModel):
    """
    Linear progression model with plateau.
    
    Equation: M(n) = min(S + (a*n)/b, T)
    where:
        M(n) = mileage at week n
        T = target mileage (plateau)
        S = starting mileage
        a = growth rate numerator
        b = growth rate denominator
    """
    
    def _validate_parameters(self) -> None:
        """Validate linear model specific constraints."""
        if self.params.a_parameter <= 0:
            raise ValueError(
                f"Parameter 'a' must be positive for linear model, got {self.params.a_parameter}"
            )
        if self.params.b_parameter <= 0:
            raise ValueError(
                f"Parameter 'b' must be positive, got {self.params.b_parameter}"
            )
        if self.params.starting_mileage > self.params.target_mileage:
            raise ValueError(
                "Starting mileage cannot exceed target mileage"
            )
    
    def calculate_mileage(self, week: float) -> float:
        """Calculate mileage using linear progression with plateau."""
        if week < 0:
            raise ValueError(f"Week must be non-negative, got {week}")
        
        S = self.params.starting_mileage
        T = self.params.target_mileage
        rate = self.params.a_parameter / self.params.b_parameter
        
        linear_value = S + rate * week
        return min(linear_value, T)
    
    def calculate_week(self, mileage: float) -> Optional[float]:
        """Calculate week for given mileage using inverse linear."""
        S = self.params.starting_mileage
        T = self.params.target_mileage
        
        if not S <= mileage <= T:
            return None
        
        if mileage == S:
            return 0.0
        
        rate = self.params.a_parameter / self.params.b_parameter
        week = (mileage - S) / rate
        
        plateau_week = self._get_plateau_week()
        
        if week <= plateau_week:
            return week
        return plateau_week if mileage == T else None
    
    def calculate_rate_of_change(self, week: float) -> float:
        """Calculate derivative of linear function."""
        if week < 0:
            raise ValueError(f"Week must be non-negative, got {week}")
        
        plateau_week = self._get_plateau_week()
        rate = self.params.a_parameter / self.params.b_parameter
        
        return rate if week < plateau_week else 0.0
    
    def _get_plateau_week(self) -> float:
        """Calculate when plateau is reached."""
        S = self.params.starting_mileage
        T = self.params.target_mileage
        
        if S == T:
            return 0.0
        
        rate = self.params.a_parameter / self.params.b_parameter
        return (T - S) / rate
    
    @property
    def model_type(self) -> str:
        """Return model type identifier."""
        return "linear"
    
    def get_equation_latex(self) -> str:
        """Get LaTeX representation of linear equation."""
        return r"M(n) = \min(S + \frac{a \cdot n}{b}, T)"