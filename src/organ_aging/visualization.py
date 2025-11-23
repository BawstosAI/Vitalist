"""
Visualization utilities for organ aging analysis.

This module provides plotting functions for age gaps, correlations,
and other aspects of organ aging analysis.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Optional, Tuple, Dict


def plot_age_gap_distribution(df: pd.DataFrame,
                              gap_columns: Optional[List[str]] = None,
                              figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
    """
    Plot distribution of age gaps for all organs.

    Args:
        df: DataFrame with age gap columns.
        gap_columns: List of gap column names. If None, auto-detects.
        figsize: Figure size.

    Returns:
        Matplotlib figure object.

    Example:
        >>> fig = plot_age_gap_distribution(df)
        >>> plt.show()
    """
    if gap_columns is None:
        gap_columns = [col for col in df.columns if col.endswith('_age_gap')]

    n_organs = len(gap_columns)
    n_cols = min(3, n_organs)
    n_rows = (n_organs + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = np.array(axes).flatten() if n_organs > 1 else [axes]

    for idx, gap_col in enumerate(gap_columns):
        organ_name = gap_col.replace('_age_gap', '').replace('_', ' ').title()

        axes[idx].hist(df[gap_col], bins=50, edgecolor='black', alpha=0.7)
        axes[idx].axvline(0, color='red', linestyle='--', linewidth=2, label='Zero gap')
        axes[idx].set_xlabel('Age Gap (years)')
        axes[idx].set_ylabel('Count')
        axes[idx].set_title(f'{organ_name} Age Gap Distribution')
        axes[idx].legend()

        # Add statistics
        mean_gap = df[gap_col].mean()
        std_gap = df[gap_col].std()
        axes[idx].text(0.02, 0.98, f'Mean: {mean_gap:.2f}±{std_gap:.2f}',
                      transform=axes[idx].transAxes,
                      verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Hide unused subplots
    for idx in range(n_organs, len(axes)):
        axes[idx].axis('off')

    plt.tight_layout()
    return fig


def plot_gap_correlation_heatmap(corr_matrix: pd.DataFrame,
                                 figsize: Tuple[int, int] = (10, 8),
                                 cmap: str = 'coolwarm') -> plt.Figure:
    """
    Plot heatmap of correlations between organ age gaps.

    Args:
        corr_matrix: Correlation matrix DataFrame.
        figsize: Figure size.
        cmap: Colormap name.

    Returns:
        Matplotlib figure object.

    Example:
        >>> corr = calculate_gap_correlations(df)
        >>> fig = plot_gap_correlation_heatmap(corr)
        >>> plt.show()
    """
    # Clean up labels
    labels = [col.replace('_age_gap', '').replace('_', ' ').title()
              for col in corr_matrix.columns]

    fig, ax = plt.subplots(figsize=figsize)

    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap=cmap,
                center=0, vmin=-1, vmax=1,
                xticklabels=labels, yticklabels=labels,
                square=True, ax=ax)

    ax.set_title('Organ Age Gap Correlations', fontsize=14, fontweight='bold')

    plt.tight_layout()
    return fig


def plot_gaps_vs_age(df: pd.DataFrame,
                    gap_columns: Optional[List[str]] = None,
                    age_col: str = 'AGE',
                    figsize: Tuple[int, int] = (14, 10)) -> plt.Figure:
    """
    Plot age gaps vs chronological age for all organs.

    Args:
        df: DataFrame with age and gap columns.
        gap_columns: List of gap column names. If None, auto-detects.
        age_col: Name of the age column.
        figsize: Figure size.

    Returns:
        Matplotlib figure object.

    Example:
        >>> fig = plot_gaps_vs_age(df)
        >>> plt.show()
    """
    if gap_columns is None:
        gap_columns = [col for col in df.columns if col.endswith('_age_gap')]

    n_organs = len(gap_columns)
    n_cols = min(3, n_organs)
    n_rows = (n_organs + n_cols - 1) // n_cols

    fig, axes = plt.subplots(n_rows, n_cols, figsize=figsize)
    axes = np.array(axes).flatten() if n_organs > 1 else [axes]

    for idx, gap_col in enumerate(gap_columns):
        organ_name = gap_col.replace('_age_gap', '').replace('_', ' ').title()

        axes[idx].scatter(df[age_col], df[gap_col], alpha=0.3, s=10)
        axes[idx].axhline(0, color='red', linestyle='--', linewidth=2)
        axes[idx].set_xlabel('Chronological Age (years)')
        axes[idx].set_ylabel('Age Gap (years)')
        axes[idx].set_title(f'{organ_name}')
        axes[idx].grid(True, alpha=0.3)

    # Hide unused subplots
    for idx in range(n_organs, len(axes)):
        axes[idx].axis('off')

    fig.suptitle('Organ Age Gaps vs Chronological Age', fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig


def plot_trajectory(trajectory_data: Dict[str, pd.DataFrame],
                   figsize: Tuple[int, int] = (12, 8)) -> plt.Figure:
    """
    Plot pseudo-longitudinal trajectories for organ age gaps.

    Args:
        trajectory_data: Dictionary mapping organ names to trajectory DataFrames.
        figsize: Figure size.

    Returns:
        Matplotlib figure object.

    Example:
        >>> trajectories = pseudo_longitudinal_analysis(df, gap_columns)
        >>> fig = plot_trajectory(trajectories)
        >>> plt.show()
    """
    fig, ax = plt.subplots(figsize=figsize)

    for organ_name, trajectory_df in trajectory_data.items():
        ax.plot(trajectory_df['age_mean'], trajectory_df['gap_mean'],
               marker='o', label=organ_name.replace('_', ' ').title(), linewidth=2)

        # Add error bars
        ax.fill_between(trajectory_df['age_mean'],
                       trajectory_df['gap_mean'] - trajectory_df['gap_std'],
                       trajectory_df['gap_mean'] + trajectory_df['gap_std'],
                       alpha=0.2)

    ax.axhline(0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax.set_xlabel('Mean Chronological Age (years)', fontsize=12)
    ax.set_ylabel('Mean Age Gap (years)', fontsize=12)
    ax.set_title('Pseudo-Longitudinal Organ Aging Trajectories', fontsize=14, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_individual_profile(df: pd.DataFrame,
                           individual_id: int,
                           gap_columns: Optional[List[str]] = None,
                           id_col: str = 'SEQN',
                           age_col: str = 'AGE',
                           figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
    """
    Plot organ aging profile for a single individual.

    Args:
        df: DataFrame with individual data.
        individual_id: ID of the individual to plot.
        gap_columns: List of gap column names. If None, auto-detects.
        id_col: Name of the ID column.
        age_col: Name of the age column.
        figsize: Figure size.

    Returns:
        Matplotlib figure object.

    Example:
        >>> fig = plot_individual_profile(df, individual_id=12345)
        >>> plt.show()
    """
    if gap_columns is None:
        gap_columns = [col for col in df.columns if col.endswith('_age_gap')]

    individual = df[df[id_col] == individual_id]

    if len(individual) == 0:
        raise ValueError(f"Individual ID {individual_id} not found")

    individual = individual.iloc[0]

    organ_names = [col.replace('_age_gap', '').replace('_', ' ').title()
                  for col in gap_columns]
    gaps = [individual[col] for col in gap_columns]

    fig, ax = plt.subplots(figsize=figsize)

    colors = ['red' if gap > 5 else 'orange' if gap > 0 else 'green' for gap in gaps]

    ax.barh(organ_names, gaps, color=colors, alpha=0.7, edgecolor='black')
    ax.axvline(0, color='black', linestyle='-', linewidth=2)
    ax.axvline(5, color='red', linestyle='--', linewidth=1, alpha=0.5, label='Advanced threshold (+5y)')
    ax.axvline(-5, color='green', linestyle='--', linewidth=1, alpha=0.5, label='Young threshold (-5y)')

    ax.set_xlabel('Age Gap (years)', fontsize=12)
    ax.set_title(f'Organ Aging Profile - Individual {individual_id} (Age: {individual[age_col]:.0f})',
                fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, axis='x', alpha=0.3)

    plt.tight_layout()
    return fig


def plot_model_comparison(comparison_df: pd.DataFrame,
                         metric: str = 'mae',
                         figsize: Tuple[int, int] = (10, 6)) -> plt.Figure:
    """
    Plot comparison of model performance across organs.

    Args:
        comparison_df: DataFrame with model comparison results.
        metric: Metric to plot ('mae', 'rmse', 'r2').
        figsize: Figure size.

    Returns:
        Matplotlib figure object.

    Example:
        >>> comparison = compare_models(models_metrics)
        >>> fig = plot_model_comparison(comparison, metric='mae')
        >>> plt.show()
    """
    fig, ax = plt.subplots(figsize=figsize)

    if metric not in comparison_df.columns:
        raise ValueError(f"Metric '{metric}' not found in comparison DataFrame")

    comparison_df = comparison_df.sort_values(metric, ascending=(metric != 'r2'))

    ax.barh(comparison_df['model_name'], comparison_df[metric],
           edgecolor='black', alpha=0.7)

    ax.set_xlabel(metric.upper(), fontsize=12)
    ax.set_title(f'Model Performance Comparison ({metric.upper()})',
                fontsize=14, fontweight='bold')
    ax.grid(True, axis='x', alpha=0.3)

    plt.tight_layout()
    return fig
