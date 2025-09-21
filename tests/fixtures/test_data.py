"""Test data fixtures."""

# Sample test data for various scenarios
SAMPLE_EXPONENTIAL_PARAMS = {
    "target_mileage": 50.0,
    "starting_mileage": 10.0,
    "a_parameter": 0.8,
    "b_parameter": 4.0
}

SAMPLE_LINEAR_PARAMS = {
    "target_mileage": 50.0,
    "starting_mileage": 10.0,
    "a_parameter": 2.0,
    "b_parameter": 1.0
}

# Expected values for testing
EXPONENTIAL_WEEK_4_MILEAGE = 20.48  # Approximate
LINEAR_WEEK_4_MILEAGE = 18.0  # Exact

# Test cases for edge scenarios
EDGE_CASES = [
    {"week": 0, "expected_mileage": "starting_mileage"},
    {"week": float('inf'), "expected_mileage": "target_mileage"},
    {"week": -1, "expected_error": ValueError},
]