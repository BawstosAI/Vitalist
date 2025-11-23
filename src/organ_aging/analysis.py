"""
Analysis utilities for organ aging patterns.

This module provides functions for analyzing age gaps, identifying patterns,
and exploring organ-specific aging trajectories.
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple


def bin_by_age(df: pd.DataFrame,
               bins: Optional[List[int]] = None,
               age_col: str = 'AGE',
               bin_col: str = 'age_bin') -> pd.DataFrame:
    """
    Bin individuals by age groups.

    Args:
        df: Input DataFrame.
        bins: List of bin edges (e.g., [18, 30, 40, 50, 60, 70, 80]).
              If None, uses default decade bins.
        age_col: Name of the age column.
        bin_col: Name for the new bin column.

    Returns:
        DataFrame with added age bin column.

    Example:
        >>> df_binned = bin_by_age(df, bins=[18, 30, 40, 50, 60, 70, 80])
        >>> print(df_binned['age_bin'].value_counts())
    """
    if bins is None:
        # Default decade bins
        bins = list(range(10, 101, 10))

    df_binned = df.copy()
    df_binned[bin_col] = pd.cut(
        df_binned[age_col],
        bins=bins,
        include_lowest=True,
        right=False
    )

    print(f"Created {df_binned[bin_col].nunique()} age bins")
    print(df_binned[bin_col].value_counts().sort_index())

    return df_binned


def calculate_gap_correlations(df: pd.DataFrame,
                               gap_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Calculate correlations between organ age gaps.

    Args:
        df: DataFrame containing age gap columns.
        gap_columns: List of gap column names. If None, auto-detects columns ending with '_age_gap'.

    Returns:
        Correlation matrix as DataFrame.

    Example:
        >>> corr_matrix = calculate_gap_correlations(df)
        >>> print(corr_matrix)
    """
    if gap_columns is None:
        gap_columns = [col for col in df.columns if col.endswith('_age_gap')]

    if not gap_columns:
        raise ValueError("No age gap columns found in DataFrame")

    corr_matrix = df[gap_columns].corr()

    print(f"\nCorrelations between {len(gap_columns)} organ age gaps:")
    print(corr_matrix)

    return corr_matrix


def identify_advanced_organs(df: pd.DataFrame,
                            threshold: float = 5.0,
                            gap_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Identify organs that are biologically advanced (age gap > threshold).

    Args:
        df: DataFrame containing age gap columns.
        threshold: Threshold for considering an organ "advanced" (years).
        gap_columns: List of gap column names. If None, auto-detects.

    Returns:
        DataFrame with added boolean columns indicating advanced organs.

    Example:
        >>> df_flagged = identify_advanced_organs(df, threshold=5.0)
        >>> print(df_flagged[['liver_advanced', 'kidney_advanced']].sum())
    """
    if gap_columns is None:
        gap_columns = [col for col in df.columns if col.endswith('_age_gap')]

    df_flagged = df.copy()

    for gap_col in gap_columns:
        organ_name = gap_col.replace('_age_gap', '')
        advanced_col = f"{organ_name}_advanced"

        df_flagged[advanced_col] = df_flagged[gap_col] > threshold

        n_advanced = df_flagged[advanced_col].sum()
        pct_advanced = 100 * n_advanced / len(df_flagged)

        print(f"{organ_name}: {n_advanced} ({pct_advanced:.1f}%) individuals with gap > {threshold} years")

    return df_flagged


def analyze_cooccurrence(df: pd.DataFrame,
                        organ_cols: List[str],
                        min_count: int = 10) -> Dict:
    """
    Analyze co-occurrence patterns of advanced organs.

    Args:
        df: DataFrame with boolean columns indicating advanced organs.
        organ_cols: List of boolean column names for advanced organs.
        min_count: Minimum count to include in results.

    Returns:
        Dictionary with co-occurrence statistics.

    Example:
        >>> cooccur = analyze_cooccurrence(df, ['liver_advanced', 'kidney_advanced'])
    """
    # Count combinations
    combinations = df[organ_cols].value_counts()
    combinations = combinations[combinations >= min_count].sort_values(ascending=False)

    # Calculate percentage of individuals with multiple organs advanced
    n_advanced_any = (df[organ_cols].sum(axis=1) > 0).sum()
    n_advanced_multiple = (df[organ_cols].sum(axis=1) > 1).sum()

    results = {
        'combinations': combinations.to_dict(),
        'n_any_advanced': n_advanced_any,
        'n_multiple_advanced': n_advanced_multiple,
        'pct_multiple': 100 * n_advanced_multiple / len(df) if len(df) > 0 else 0
    }

    print(f"\nCo-occurrence Analysis:")
    print(f"  Individuals with any organ advanced: {n_advanced_any} ({100*n_advanced_any/len(df):.1f}%)")
    print(f"  Individuals with multiple organs advanced: {n_advanced_multiple} ({results['pct_multiple']:.1f}%)")
    print(f"\nTop combinations (count >= {min_count}):")
    for combination, count in list(combinations.items())[:10]:
        print(f"  {combination}: {count}")

    return results


def analyze_gaps_by_age_group(df: pd.DataFrame,
                              gap_columns: Optional[List[str]] = None,
                              age_col: str = 'AGE',
                              bins: Optional[List[int]] = None) -> pd.DataFrame:
    """
    Analyze how organ age gaps vary across age groups.

    Args:
        df: DataFrame with age and gap columns.
        gap_columns: List of gap column names. If None, auto-detects.
        age_col: Name of the age column.
        bins: Age bin edges.

    Returns:
        DataFrame with mean gaps by age group.

    Example:
        >>> gap_by_age = analyze_gaps_by_age_group(df)
    """
    if gap_columns is None:
        gap_columns = [col for col in df.columns if col.endswith('_age_gap')]

    # Bin by age
    df_binned = bin_by_age(df, bins=bins, age_col=age_col)

    # Calculate mean gaps by age bin
    gap_by_age = df_binned.groupby('age_bin')[gap_columns].agg(['mean', 'std', 'count'])

    print("\nMean age gaps by age group:")
    print(gap_by_age)

    return gap_by_age


def identify_fastest_aging_organs(df: pd.DataFrame,
                                  gap_columns: Optional[List[str]] = None,
                                  per_individual: bool = True) -> pd.DataFrame:
    """
    Identify which organ is aging fastest for each individual or population.

    Args:
        df: DataFrame with age gap columns.
        gap_columns: List of gap column names. If None, auto-detects.
        per_individual: If True, identify fastest aging organ per individual.
                       If False, rank by population mean.

    Returns:
        If per_individual=True: DataFrame with added 'fastest_aging_organ' column.
        If per_individual=False: DataFrame with organs ranked by mean gap.

    Example:
        >>> df_fastest = identify_fastest_aging_organs(df, per_individual=True)
        >>> print(df_fastest['fastest_aging_organ'].value_counts())
    """
    if gap_columns is None:
        gap_columns = [col for col in df.columns if col.endswith('_age_gap')]

    if per_individual:
        df_result = df.copy()

        # Find organ with largest gap for each individual
        df_result['fastest_aging_organ'] = df[gap_columns].idxmax(axis=1)
        df_result['fastest_aging_organ'] = df_result['fastest_aging_organ'].str.replace('_age_gap', '')

        df_result['max_age_gap'] = df[gap_columns].max(axis=1)

        print("\nFastest aging organ distribution:")
        print(df_result['fastest_aging_organ'].value_counts())

        return df_result

    else:
        # Population-level ranking
        mean_gaps = df[gap_columns].mean().sort_values(ascending=False)
        organ_names = [col.replace('_age_gap', '') for col in mean_gaps.index]

        ranking_df = pd.DataFrame({
            'organ': organ_names,
            'mean_age_gap': mean_gaps.values
        })

        print("\nOrgans ranked by population mean age gap:")
        print(ranking_df)

        return ranking_df


def calculate_gap_variability(df: pd.DataFrame,
                              gap_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Calculate variability metrics for organ age gaps.

    Args:
        df: DataFrame with age gap columns.
        gap_columns: List of gap column names. If None, auto-detects.

    Returns:
        DataFrame with variability metrics (std, IQR, coefficient of variation).

    Example:
        >>> variability = calculate_gap_variability(df)
    """
    if gap_columns is None:
        gap_columns = [col for col in df.columns if col.endswith('_age_gap')]

    metrics = []

    for gap_col in gap_columns:
        organ_name = gap_col.replace('_age_gap', '')
        values = df[gap_col]

        metrics.append({
            'organ': organ_name,
            'mean': values.mean(),
            'std': values.std(),
            'iqr': values.quantile(0.75) - values.quantile(0.25),
            'cv': values.std() / abs(values.mean()) if values.mean() != 0 else np.nan,
            'min': values.min(),
            'max': values.max()
        })

    variability_df = pd.DataFrame(metrics)
    variability_df = variability_df.sort_values('std', ascending=False)

    print("\nOrgan age gap variability:")
    print(variability_df)

    return variability_df


def pseudo_longitudinal_analysis(df: pd.DataFrame,
                                gap_columns: List[str],
                                age_col: str = 'AGE',
                                age_bins: Optional[List[int]] = None) -> Dict[str, pd.DataFrame]:
    """
    Perform pseudo-longitudinal analysis by examining gaps across age groups.

    This simulates longitudinal trends using cross-sectional data.

    Args:
        df: DataFrame with age and gap columns.
        gap_columns: List of gap column names.
        age_col: Name of the age column.
        age_bins: Age bin edges.

    Returns:
        Dictionary containing trajectory DataFrames for each organ.

    Example:
        >>> trajectories = pseudo_longitudinal_analysis(df, gap_columns)
    """
    df_binned = bin_by_age(df, bins=age_bins, age_col=age_col)

    trajectories = {}

    for gap_col in gap_columns:
        organ_name = gap_col.replace('_age_gap', '')

        trajectory = df_binned.groupby('age_bin').agg({
            gap_col: ['mean', 'std', 'count'],
            age_col: 'mean'
        }).reset_index()

        trajectory.columns = ['age_bin', 'gap_mean', 'gap_std', 'n_samples', 'age_mean']

        trajectories[organ_name] = trajectory

        print(f"\n{organ_name} trajectory:")
        print(trajectory)

    return trajectories
