#Setup configuration for the package.

from setuptools import setup, find_packages

# Check if README exists, if not create a simple one
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = "Runner Training System - A comprehensive training progression calculator"

setup(
    name="runner-training-system",
    version="2.0.0",
    author="Neha Thottathil",
    author_email="nthottathil@live.co.uk",
    description="Advanced training progression calculator with multiple models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nthottathil/Runna",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.10",
    install_requires=[
        "fastapi>=0.104.0",
        "uvicorn[standard]>=0.24.0",
        "pydantic>=2.5.0",
        "pydantic-settings>=2.1.0",
        "python-dotenv>=1.0.0",
        "matplotlib>=3.8.0",
        "numpy>=1.26.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-asyncio>=0.21.0",
            "httpx>=0.25.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "isort>=5.13.0",
            "pre-commit>=3.6.0",
        ],
    },
)