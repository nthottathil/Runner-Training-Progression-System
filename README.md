# Runner Training Progression System 

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Coverage](https://img.shields.io/badge/coverage-75%25-green)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

A mathematical model-based API for calculating optimal running mileage progression to prevent injuries while maximising training efficiency.

## Table of Contents
- [Problem Statement](#problem-statement)
- [Solution Approach](#solution-approach)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Technical Decisions](#technical-decisions)
- [Future Enhancements](#future-enhancements)

## Problem Statement

### The Challenge
Runners face a critical dilemma when increasing their training volume:
- **Too Fast**: Increasing mileage too quickly leads to injuries, [at least 50% of regular runners get injured every year](https://www.yalemedicine.org/conditions/running-injury)
- **Too Slow**: Conservative progression wastes valuable training time
- **Individual Variation**: Each runner adapts differently based on age, fitness, and history

### The Solution
Mathematical models that calculate personalised, optimal weekly mileage progression based on proven training principles and physiological adaptation curves.

## Solution Approach

### My Thought Process
Initial Thinking:
1. Research Phase: Studied how runners typically progress([10-20% rule](https://www.runna.com/blog)) everything-you-need-to-know-about-embracing-your-easy-runs), periodisation)
2. Mathematical Modeling: Found exponential growth generally mirrors human adaptation
3. Implementation: Started simple, iteratively added complexity
4. Validation: Compared outputs with real training plans

Key Insight: [Human adaptation generally follows exponential](https://www.aurumfit.com/blog/hit-training-part1) curves with rapid initial gains that gradually plateau. This is seen in strength training, skill acquisition, and endurance building.

### Mathematical Models

#### 1. Exponential Model (Primary)
```
M(n) = T - (T - S) × a^(n/b)

Where:
- M(n) = Mileage at week n
- T = Target mileage (default: 50 miles)
- S = Starting mileage (default: 10 miles)  
- a = Decay parameter (0 < a < 1, default: 0.8)
- b = Time scaling factor (default: 4)
```

**Rationale**: Mimics physiological adaptation - aggressive early gains when body is responsive, conservative later to prevent overtraining.

#### 2. Linear Model (Alternative)
```
M(n) = min(S + (a×n)/b, T)
```

**Rationale**: Simpler model for beginners or rehabilitation scenarios where consistent, predictable progression is preferred.

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/nthottathil/runner-training-system.git
cd runner-training-system

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # for Windows user
# source venv/bin/activate  # for Mac/Linux users

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the server
python scripts/run_server.py

# 5. Open browser
# Visit: http://localhost:8000/docs
```

## Installation

### Prerequisites
- [Python 3.10 or higher](https://www.python.org/downloads/)
- [pip package manager](https://pip.pypa.io/en/stable/installation/)
- [Git](https://git-scm.com/downloads)

### Detailed Setup

1. **Clone the repository**
```bash
git clone https://github.com/nthottathil/runner-training-system.git
cd runner-training-system
```

2. **Create and activate virtual environment**
```bash
# For Windows users
python -m venv venv
venv\Scripts\activate

# For Mac/Linux users
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
# Production dependencies only
pip install -r requirements.txt

# Development dependencies (includes testing tools)
pip install -r requirements-dev.txt
```

4. **Configure environment variables**
```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your preferences
# TARGET_MILEAGE=50.0
# STARTING_MILEAGE=10.0
# A_PARAMETER=0.8
# B_PARAMETER=4.0
# EQUATION_CHOICE=exponential
```

## Running the Application

### Start the API Server

```bash
# Using the run script
python scripts/run_server.py
```

You should see:
```
Runner Training API Server
==================================================
Model Type: exponential
Target Mileage: 50.0 miles
Starting Mileage: 10.0 miles
Parameters: a=0.8, b=4.0
==================================================
Server: http://127.0.0.1:8000
API Docs: http://127.0.0.1:8000/docs
```

### Generate Visualisations

```bash
python scripts/visualise_models.py
```

This creates:
- `exponential_progression.png` - Exponential model visualisation
- `linear_progression.png` - Linear model visualisation  
- `model_comparison.png` - Side-by-side comparison

## API Documentation

### Interactive Documentation
Visit http://localhost:8000/docs for Swagger UI with "Try it out" functionality. Make sure the server is still running. Run `python scripts/run_server.py` again if needed.

### Endpoints

#### 1. Calculate Mileage for a Given Week
```http
POST /api/v1/calculate-mileage
Content-Type: application/json

{
  "week_number": 4,
  "target_mileage": 50.0,    # Optional override
  "starting_mileage": 10.0,  # Optional override
  "a_parameter": 0.8,        # Optional override
  "b_parameter": 4.0         # Optional override
}
```

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/api/v1/calculate-mileage" \
  -H "Content-Type: application/json" \
  -d '{"week_number": 4}'
```

**Example using PowerShell:**
```powershell
$body = @{week_number = 4} | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/api/v1/calculate-mileage" `
  -Method POST -Body $body -ContentType "application/json"
```

**Response:**
```json
{
  "week_number": 4,
  "weekly_mileage": 20.48,
  "percentage_of_target": 40.96,
  "equation_type": "exponential",
  "parameters": {
    "model_type": "exponential",
    "target_mileage": 50.0,
    "starting_mileage": 10.0,
    "a_parameter": 0.8,
    "b_parameter": 4.0
  }
}
```

#### 2. Calculate Week to Reach Target Mileage
```http
POST /api/v1/calculate-week
Content-Type: application/json

{
  "weekly_mileage": 30.0
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v1/calculate-week" \
  -H "Content-Type: application/json" \
  -d '{"weekly_mileage": 30}'
```

**Response:**
```json
{
  "weekly_mileage": 30.0,
  "week_number": 7.58,
  "is_achievable": true,
  "message": null,
  "equation_type": "exponential",
  "parameters": {...}
}
```

#### 3. Calculate Rate of Change
```http
POST /api/v1/rate-of-change
Content-Type: application/json

{
  "week_number": 6
}
```

**Response:**
```json
{
  "week_number": 6,
  "rate_of_change": 2.3456,
  "interpretation": "At week 6, mileage increases by 2.346 miles per week",
  "equation_type": "exponential",
  "parameters": {...}
}
```

#### 4. Get Visualisation Data
```http
POST /api/v1/visualise
Content-Type: application/json

{
  "weeks_to_plot": 20,
  "include_rate": true
}
```

#### 5. Health Check
```http
GET /api/v1/health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "equation_type": "exponential",
  "default_parameters": {...}
}
```

## Testing

### Run All Tests
```bash
# Run all tests with coverage
pytest --cov=src/runner_training --cov-report=html

# Run specific test categories
pytest -m unit          # Unit tests only
pytest -m integration   # Integration tests only

# Run with verbose output
pytest -v
```

### Test Structure
```
tests/
├── unit/
│   ├── test_models.py      # Model calculations
│   └── test_validators.py  # Input validation
└── integration/
    └── test_api.py         # API endpoints
```

### Example Test
```python
def test_exponential_progression():
    """
    Thought Process: Test that mileage increases but never exceeds target
    Edge Cases: Week 0, negative weeks, very large weeks
    """
    model = ExponentialModel(params)
    
    # Test progression increases
    week_0 = model.calculate_mileage(0)
    week_4 = model.calculate_mileage(4)
    week_8 = model.calculate_mileage(8)
    
    assert week_0 < week_4 < week_8 < target_mileage
    assert week_8 - week_4 < week_4 - week_0  # Diminishing returns
```

## Project Structure

```
runner-training-system/
├── src/
│   └── runner_training/
│       ├── models/          # Core logic
│       │   ├── base.py     # Abstract base class (enforces interface)
│       │   ├── exponential.py  # Exponential progression model
│       │   ├── linear.py   # Linear progression model
│       │   └── factory.py  # Model creation (factory pattern)
│       ├── api/
│       │   ├── server.py   # FastAPI application setup
│       │   ├── routes.py   # API endpoint handlers
│       │   └── schemas.py  # Request/response models (Pydantic)
│       ├── config/
│       │   └── settings.py # Environment configuration
│       ├── utils/
│       │   └── validators.py  # Input validation helpers
│       └── visualisation/
│           └── plotter.py  # Matplotlib visualisations
├── tests/                  # Comprehensive test suite
├── scripts/               # Utility scripts
├── .env.example          # Configuration template
├── requirements.txt      # Production dependencies
├── requirements-dev.txt  # Development dependencies
├── pytest.ini           # Test configuration
└── setup.py            # Package configuration
```

## Technical Decisions

### Architecture Choices

Decision: Clean Architecture with Separation of Concerns

Reasoning:
1. Models (Domain Layer): Just the logic, no dependencies
2. API (Interface Layer): Handles HTTP, depends on models
3. Config (Infrastructure): External configuration

Benefits:
- Testability: Each layer can be tested independently
- Maintainability: Changes in one layer don't affect others
- Scalability: Easy to add new models or endpoints

### Technology Stack

| Technology | Justification |
|------------|--------------|
| **FastAPI** | Modern, fast, automatic documentation, type safety |
| **Pydantic** | Runtime validation, prevents errors reaching business logic |
| **Pytest** | Powerful testing with fixtures and parametrization |
| **Type Hints** | Self-documenting code, IDE support, error prevention |

### Design Patterns

1. **Factory Pattern**
```python
# Simplifies model creation, hides implementation details
model = ModelFactory.create("exponential", 50, 10, 0.8, 4)
```

2. **Abstract Base Class**
```python
# Ensures all models have consistent interface
class BaseTrainingModel(ABC):
    @abstractmethod
    def calculate_mileage(self, week: float) -> float:
```

3. **Dependency Injection**
```python
# Makes testing easier, configuration flexible
def create_app(settings: Settings) -> FastAPI:
```

## Future Enhancements

- **Authentication & User Management**: JWT-based authentication for personalized training plans
- **Database Integration**: PostgreSQL for storing user progress and historical data
- **Machine Learning**: Adaptive models based on individual training history
- **Wearables Integration**: Real-time adjustments based on recovery metrics
- **AI Coach**: Natural language interface for personalized training advice and motivation
- **Mobile App**: React Native app for on-the-go access

## Contributing

### Development Workflow

1. Create feature branch
```bash
git checkout -b feature/your-feature-name
```

2. Make changes and test
```bash
pytest
black src/ tests/
isort src/ tests/
```

3. Commit with descriptive message
```bash
git add .
git commit -m "feat: add recovery adjustment endpoint"
```

4. Push and create PR
```bash
git push origin feature/your-feature-name
```

## Contact

- **Author**: Neha Thottathil
- **Email**: nthottathil@live.co.uk
- **LinkedIn**: [Neha Thottathil](https://www.linkedin.com/in/neha-thottathil-8a41331b4/)
- **GitHub**: [@nthottathil](https://github.com/nthottathil)

---

