"""Integration tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient


class TestAPIEndpoints:
    """Test suite for API endpoints."""
    
    def test_health_check(self, test_client):
        """Test health check endpoint."""
        response = test_client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "equation_type" in data
    
    def test_calculate_mileage_success(self, test_client):
        """Test successful mileage calculation."""
        response = test_client.post(
            "/api/v1/calculate-mileage",
            json={"week_number": 4}
        )
        assert response.status_code == 200
        data = response.json()
        assert "weekly_mileage" in data
        assert "percentage_of_target" in data
        assert data["week_number"] == 4
    
    def test_calculate_mileage_with_overrides(self, test_client):
        """Test mileage calculation with parameter overrides."""
        response = test_client.post(
            "/api/v1/calculate-mileage",
            json={
                "week_number": 4,
                "target_mileage": 60,
                "starting_mileage": 15
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["parameters"]["target_mileage"] == 60
        assert data["parameters"]["starting_mileage"] == 15
    
    def test_calculate_mileage_invalid_week(self, test_client):
        """Test error on invalid week number."""
        response = test_client.post(
            "/api/v1/calculate-mileage",
            json={"week_number": -1}
        )
        assert response.status_code == 422  # Validation error
    
    def test_calculate_week_success(self, test_client):
        """Test successful week calculation."""
        response = test_client.post(
            "/api/v1/calculate-week",
            json={"weekly_mileage": 30}
        )
        assert response.status_code == 200
        data = response.json()
        assert "week_number" in data
        assert data["is_achievable"] == True
    
    def test_calculate_week_out_of_range(self, test_client):
        """Test week calculation for out-of-range mileage."""
        response = test_client.post(
            "/api/v1/calculate-week",
            json={"weekly_mileage": 100}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["is_achievable"] == False
        assert "outside valid range" in data["message"]
    
    def test_rate_of_change_success(self, test_client):
        """Test successful rate of change calculation."""
        response = test_client.post(
            "/api/v1/rate-of-change",
            json={"week_number": 6}
        )
        assert response.status_code == 200
        data = response.json()
        assert "rate_of_change" in data
        assert "interpretation" in data
        assert data["week_number"] == 6
    
    def test_visualisation_data(self, test_client):
        """Test visualisation data endpoint."""
        response = test_client.post(
            "/api/v1/visualise",
            json={"weeks_to_plot": 10, "include_rate": True}
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["weeks"]) == 10
        assert len(data["mileages"]) == 10
        assert len(data["rates"]) == 10
        assert "equation_latex" in data
    
    def test_visualisation_without_rates(self, test_client):
        """Test visualisation without rate data."""
        response = test_client.post(
            "/api/v1/visualise",
            json={"weeks_to_plot": 10, "include_rate": False}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["rates"] is None


class TestAPIValidation:
    """Test API input validation."""
    
    def test_negative_mileage_rejected(self, test_client):
        """Test that negative mileage is rejected."""
        response = test_client.post(
            "/api/v1/calculate-week",
            json={"weekly_mileage": -10}
        )
        assert response.status_code == 422
    
    def test_invalid_parameter_types(self, test_client):
        """Test that invalid parameter types are rejected."""
        response = test_client.post(
            "/api/v1/calculate-mileage",
            json={
                "week_number": "four"  # Should be numeric
            }
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self, test_client):
        """Test that missing required fields are rejected."""
        response = test_client.post(
            "/api/v1/calculate-mileage",
            json={}  # Missing week_number
        )
        assert response.status_code == 422