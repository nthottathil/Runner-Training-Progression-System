"""Unit tests for validators."""

import pytest
from src.runner_training.utils.validators import ParameterValidator, DataValidator


class TestParameterValidator:
    """Test suite for parameter validator."""
    
    def test_validate_mileage_range_exponential_valid(self):
        """Test valid mileage range for exponential model."""
        ParameterValidator.validate_mileage_range(10, 50, "exponential")
        # Should not raise
    
    def test_validate_mileage_range_exponential_invalid(self):
        """Test invalid mileage range for exponential model."""
        with pytest.raises(ValueError, match="must be less than target"):
            ParameterValidator.validate_mileage_range(50, 50, "exponential")
    
    def test_validate_mileage_range_linear_valid(self):
        """Test valid mileage range for linear model."""
        ParameterValidator.validate_mileage_range(10, 50, "linear")
        ParameterValidator.validate_mileage_range(50, 50, "linear")  # Equal is OK
        # Should not raise
    
    def test_validate_mileage_range_negative_target(self):
        """Test negative target mileage."""
        with pytest.raises(ValueError, match="Target mileage must be positive"):
            ParameterValidator.validate_mileage_range(10, -50, "exponential")
    
    def test_validate_model_parameters_exponential_valid(self):
        """Test valid parameters for exponential model."""
        ParameterValidator.validate_model_parameters(0.8, 4, "exponential")
        # Should not raise
    
    def test_validate_model_parameters_exponential_invalid_a(self):
        """Test invalid a parameter for exponential model."""
        with pytest.raises(ValueError, match="parameter a must be in"):
            ParameterValidator.validate_model_parameters(1.5, 4, "exponential")
    
    def test_validate_model_parameters_linear_valid(self):
        """Test valid parameters for linear model."""
        ParameterValidator.validate_model_parameters(2, 1, "linear")
        # Should not raise
    
    def test_validate_model_parameters_linear_invalid_a(self):
        """Test invalid a parameter for linear model."""
        with pytest.raises(ValueError, match="parameter a must be positive"):
            ParameterValidator.validate_model_parameters(-1, 1, "linear")
    
    def test_validate_week_number_valid(self):
        """Test valid week number."""
        ParameterValidator.validate_week_number(0)
        ParameterValidator.validate_week_number(10.5)
        # Should not raise
    
    def test_validate_week_number_invalid(self):
        """Test invalid week number."""
        with pytest.raises(ValueError, match="Week number must be non-negative"):
            ParameterValidator.validate_week_number(-1)


class TestDataValidator:
    """Test suite for data validator."""
    
    def test_validate_request_parameters_valid(self):
        """Test valid request parameters."""
        params = {
            "target_mileage": 50.0,
            "starting_mileage": 10.0,
            "a_parameter": 0.8,
            "b_parameter": 4.0
        }
        cleaned = DataValidator.validate_request_parameters(params)
        assert cleaned == params
    
    def test_validate_request_parameters_filters_none(self):
        """Test that None values are filtered."""
        params = {
            "target_mileage": 50.0,
            "starting_mileage": None,
            "a_parameter": 0.8
        }
        cleaned = DataValidator.validate_request_parameters(params)
        assert "starting_mileage" not in cleaned
        assert len(cleaned) == 2
    
    def test_validate_request_parameters_invalid_type(self):
        """Test invalid parameter type."""
        params = {
            "target_mileage": "fifty"  # Should be numeric
        }
        with pytest.raises(ValueError, match="must be numeric"):
            DataValidator.validate_request_parameters(params)