"""visualisation module for training models."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from typing import Optional, Tuple, List
from ..models.base import BaseTrainingModel
from ..config.settings import Settings


class TrainingPlotter:
    """Plotter for training progression visualisation."""
    
    def __init__(self, settings: Optional[Settings] = None):
        """Initialize plotter with settings."""
        self.settings = settings or Settings()
        plt.style.use('seaborn-v0_8-darkgrid')
    
    def plot_progression(
        self,
        model: BaseTrainingModel,
        weeks: int = 20,
        save_path: Optional[str] = None
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Plot training progression over time.
        
        Args:
            model: Training model to visualise
            weeks: Number of weeks to plot
            save_path: Optional path to save the figure
            
        Returns:
            Matplotlib figure and axes objects
        """
        week_range = np.linspace(0, weeks-1, 100)
        mileages = [model.calculate_mileage(w) for w in week_range]
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [2, 1]})
        
        # Main progression plot
        ax1.plot(week_range, mileages, 'b-', linewidth=2, label='Weekly Mileage')
        ax1.axhline(y=model.params.target_mileage, color='r', linestyle='--', alpha=0.7, label='Target')
        ax1.axhline(y=model.params.starting_mileage, color='g', linestyle='--', alpha=0.7, label='Starting')
        
        # Highlight key milestones
        milestones = [0.25, 0.5, 0.75, 0.9]
        for milestone in milestones:
            target_mileage = model.params.starting_mileage + milestone * (
                model.params.target_mileage - model.params.starting_mileage
            )
            week = model.calculate_week(target_mileage)
            if week and week != float('inf') and week < weeks:
                ax1.plot(week, target_mileage, 'ko', markersize=8)
                ax1.annotate(f'{int(milestone*100)}%', 
                           xy=(week, target_mileage),
                           xytext=(5, 5), textcoords='offset points')
        
        ax1.set_xlabel('Week', fontsize=12)
        ax1.set_ylabel('Weekly Mileage (miles)', fontsize=12)
        ax1.set_title(f'{model.model_type.capitalize()} Training Progression', fontsize=14, fontweight='bold')
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, weeks)
        
        # Rate of change plot
        rates = [model.calculate_rate_of_change(w) for w in week_range]
        ax2.plot(week_range, rates, 'orange', linewidth=2)
        ax2.fill_between(week_range, rates, alpha=0.3, color='orange')
        ax2.set_xlabel('Week', fontsize=12)
        ax2.set_ylabel('Rate of Change\n(miles/week)', fontsize=12)
        ax2.set_title('Training Intensity (Rate of Change)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, weeks)
        
        # Add equation display
        equation_text = f"Equation: {model.get_equation_latex()}"
        param_text = (f"T={model.params.target_mileage:.1f}, "
                     f"S={model.params.starting_mileage:.1f}, "
                     f"a={model.params.a_parameter:.2f}, "
                     f"b={model.params.b_parameter:.2f}")
        
        fig.text(0.5, 0.02, equation_text, ha='center', fontsize=10, style='italic')
        fig.text(0.5, 0.005, param_text, ha='center', fontsize=9)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.settings.plot_dpi, bbox_inches='tight')
        
        return fig, (ax1, ax2)
    
    def compare_models(
        self,
        models: List[BaseTrainingModel],
        weeks: int = 20,
        save_path: Optional[str] = None
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Compare multiple training models.
        
        Args:
            models: List of training models to compare
            weeks: Number of weeks to plot
            save_path: Optional path to save the figure
            
        Returns:
            Matplotlib figure and axes objects
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = ['blue', 'red', 'green', 'purple', 'orange']
        
        week_range = np.linspace(0, weeks-1, 100)
        
        for i, model in enumerate(models):
            mileages = [model.calculate_mileage(w) for w in week_range]
            color = colors[i % len(colors)]
            label = f'{model.model_type.capitalize()} (a={model.params.a_parameter:.2f}, b={model.params.b_parameter:.2f})'
            ax.plot(week_range, mileages, color=color, linewidth=2, label=label)
        
        ax.set_xlabel('Week', fontsize=12)
        ax.set_ylabel('Weekly Mileage (miles)', fontsize=12)
        ax.set_title('Model Comparison', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, weeks)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=self.settings.plot_dpi, bbox_inches='tight')
        
        return fig, ax