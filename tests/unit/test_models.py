"""Unit tests for training models."""

import pytest
import math
from src.runner_training.models.exponential import ExponentialModel
from src.runner_training.models.linear import LinearModel
from src.runner_training.models.factory import ModelFactory
from src.runner_training.models.base import ModelParameters


class TestExponentialModel:
    """Test suite for exponential model."""
    
    def test_initialization_valid(self, exponential_params):
        """Test valid model initialization."""
        model = ExponentialModel(exponential_params)
        assert model.params == exponential_params
        assert model.model_type == "exponential"
    
    def test_initialization_invalid_a_parameter(self):
        """Test initialization with invalid a parameter."""
        with pytest.raises(ValueError, match="Parameter 'a' must be in"):
            params = ModelParameters(50, 10, 1.5, 4)  # a > 1
            ExponentialModel(params)
    
    def test_calculate_mileage_week_zero(self, exponential_params):
        """Test mileage calculation at week 0."""
        model = ExponentialModel(exponential_params)
        mileage = model.calculate_mileage(0)
        assert abs(mileage - 10.0) < 1e-10
    
    def test_calculate_mileage_progression(self, exponential_params):
        """Test mileage increases over time."""
        model = ExponentialModel(exponential_params)
        week4 = model.calculate_mileage(4)
        week8 = model.calculate_mileage(8)
        week12 = model.calculate_mileage(12)
        
        assert 10 < week4 < week8 < week12 < 50
        assert week8 - week4 < week4 - 10  # Diminishing returns
    
    def test_calculate_mileage_negative_week(self, exponential_params):
        """Test error on negative week."""
        model = ExponentialModel(exponential_params)
        with pytest.raises(ValueError, match="Week must be non-negative"):
            model.calculate_mileage(-1)
    
    def test_calculate_week_valid_mileage(self, exponential_params):
        """Test week calculation for valid mileage."""
        model = ExponentialModel(exponential_params)
        mileage = model.calculate_mileage(6)
        recovered_week = model.calculate_week(mileage)
        assert abs(recovered_week - 6) < 1e-6
    
    def test_calculate_week_target_mileage(self, exponential_params):
        """Test week calculation for target mileage."""
        model = ExponentialModel(exponential_params)
        week = model.calculate_week(50.0)
        assert week == float('inf')
    
    def test_calculate_week_out_of_range(self, exponential_params):
        """Test week calculation for out-of-range mileage."""
        model = ExponentialModel(exponential_params)
        assert model.calculate_week(5.0) is None  # Below starting
        assert model.calculate_week(60.0) is None  # Above target
    
    def test_rate_of_change_decreasing(self, exponential_params):
        """Test rate of change decreases over time."""
        model = ExponentialModel(exponential_params)
        rate2 = model.calculate_rate_of_change(2)
        rate6 = model.calculate_rate_of_change(6)
        rate10 = model.calculate_rate_of_change(10)
        
        assert rate2 > rate6 > rate10 > 0
        assert all(r > 0 for r in [rate2, rate6, rate10])
    
    def test_equation_latex(self, exponential_params):
        """Test LaTeX equation generation."""
        model = ExponentialModel(exponential_params)
        latex = model.get_equation_latex()
        assert "M(n)" in latex
        assert "a^{n/b}" in latex


class TestLinearModel:
    """Test suite for linear model."""
    
    def test_initialization_valid(self, linear_params):
        """Test valid model initialization."""
        model = LinearModel(linear_params)
        assert model.params == linear_params
        assert model.model_type == "linear"
    
    def test_initialization_invalid_a_parameter(self):
        """Test initialization with invalid a parameter."""
        with pytest.raises(ValueError, match="Parameter 'a' must be positive"):
            params = ModelParameters(50, 10, -1, 1)  # a < 0
            LinearModel(params)
    
    def test_calculate_mileage_linear_progression(self, linear_params):
        """Test linear mileage progression."""
        model = LinearModel(linear_params)
        week0 = model.calculate_mileage(0)
        week1 = model.calculate_mileage(1)
        week2 = model.calculate_mileage(2)
        
        assert week0 == 10.0
        assert week1 == 12.0  # 10 + (2*1)/1
        assert week2 == 14.0  # 10 + (2*2)/1
        
        # Check constant rate
        assert (week2 - week1) == (week1 - week0)
    
    def test_calculate_mileage_plateau(self, linear_params):
        """Test plateau behavior."""
        model = LinearModel(linear_params)
        week30 = model.calculate_mileage(30)
        week40 = model.calculate_mileage(40)
        
        assert week30 == 50.0  # Should plateau at target
        assert week40 == 50.0
    
    def test_calculate_week_valid_mileage(self, linear_params):
        """Test week calculation for valid mileage."""
        model = LinearModel(linear_params)
        week = model.calculate_week(30.0)
        assert abs(week - 10.0) < 1e-10  # (30-10)/(2/1) = 10
    
    def test_rate_of_change_constant_then_zero(self, linear_params):
        """Test rate of change is constant then zero."""
        model = LinearModel(linear_params)
        rate5 = model.calculate_rate_of_change(5)
        rate10 = model.calculate_rate_of_change(10)
        rate25 = model.calculate_rate_of_change(25)  # After plateau
        
        assert abs(rate5 - 2.0) < 1e-10
        assert abs(rate10 - 2.0) < 1e-10
        assert abs(rate25 - 0.0) < 1e-10
    
    def test_plateau_week_calculation(self, linear_params):
        """Test plateau week calculation."""
        model = LinearModel(linear_params)
        plateau_week = model._get_plateau_week()
        assert abs(plateau_week - 20.0) < 1e-10  # (50-10)/(2/1) = 20


class TestModelFactory:
    """Test suite for model factory."""
    
    def test_create_exponential_model(self):
        """Test creating exponential model."""
        model = ModelFactory.create("exponential", 50, 10, 0.8, 4)
        assert isinstance(model, ExponentialModel)
        assert model.model_type == "exponential"
    
    def test_create_linear_model(self):
        """Test creating linear model."""
        model = ModelFactory.create("linear", 50, 10, 2, 1)
        assert isinstance(model, LinearModel)
        assert model.model_type == "linear"
    
    def test_create_case_insensitive(self):
        """Test case-insensitive model creation."""
        model1 = ModelFactory.create("EXPONENTIAL", 50, 10, 0.8, 4)
        model2 = ModelFactory.create("Linear", 50, 10, 2, 1)
        
        assert isinstance(model1, ExponentialModel)
        assert isinstance(model2, LinearModel)
    
    def test_create_invalid_type(self):
        """Test error on invalid model type."""
        with pytest.raises(ValueError, match="Unknown model type"):
            ModelFactory.create("invalid", 50, 10, 0.8, 4)
    
    def test_available_models(self):
        """Test listing available models."""
        models = ModelFactory.available_models()
        assert "exponential" in models
        assert "linear" in models
        assert len(models) >= 2