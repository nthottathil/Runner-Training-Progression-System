#!/usr/bin/env python3
"""Script to visualise and compare training models."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import matplotlib.pyplot as plt
from src.runner_training.models.factory import ModelFactory
from src.runner_training.visualisation.plotter import TrainingPlotter
from src.runner_training.config.settings import Settings


def main():
    """Generate visualisation comparisons."""
    settings = Settings()
    plotter = TrainingPlotter(settings)
    
    # Create models
    exp_model = ModelFactory.create(
        "exponential",
        settings.target_mileage,
        settings.starting_mileage,
        settings.a_parameter,
        settings.b_parameter
    )
    
    lin_model = ModelFactory.create(
        "linear",
        settings.target_mileage,
        settings.starting_mileage,
        2.0,  # Different parameters for comparison
        1.0
    )
    
    # Individual model visualisation
    print("Generating individual model visualisations...")
    fig1, axes1 = plotter.plot_progression(
        exp_model,
        weeks=settings.plot_weeks,
        save_path="exponential_progression.png"
    )
    print("Saved: exponential_progression.png")
    
    fig2, axes2 = plotter.plot_progression(
        lin_model,
        weeks=settings.plot_weeks,
        save_path="linear_progression.png"
    )
    print("Saved: linear_progression.png")
    
    # Model comparison
    print("Generating model comparison...")
    fig3, ax3 = plotter.compare_models(
        [exp_model, lin_model],
        weeks=settings.plot_weeks,
        save_path="model_comparison.png"
    )
    print("Saved: model_comparison.png")
    
    # Show plots
    plt.show()
    
    print("\nVisualisations complete!")


if __name__ == "__main__":
    main()