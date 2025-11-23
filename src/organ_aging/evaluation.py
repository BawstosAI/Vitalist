"""
Model evaluation and age gap computation.

This module provides functions for evaluating organ clock models
and computing biological age gaps.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Any
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate regression metrics for age prediction.

    Args:
        y_true: True age values.
        y_pred: Predicted age values.

    Returns:
        Dictionary containing MAE, RMSE, and R² metrics.

    Example:
        >>> y_true = np.array([25, 35, 45, 55])
        >>> y_pred = np.array([26, 34, 46, 54])
        >>> metrics = calculate_metrics(y_true, y_pred)
        >>> print(f"MAE: {metrics['mae']:.2f}")
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)

    return {
        'mae': mae,
        'rmse': rmse,
        'r2': r2
    }


def evaluate_model(model: Any,
                  X: pd.DataFrame,
                  y: pd.Series,
                  dataset_name: str = "test") -> Dict[str, float]:
    """
    Evaluate a model on a dataset and print metrics.

    Args:
        model: Trained model with predict method.
        X: Feature matrix.
        y: True target values.
        dataset_name: Name of the dataset (for printing).

    Returns:
        Dictionary of metrics.

    Example:
        >>> metrics = evaluate_model(model, X_test, y_test, dataset_name="test")
    """
    y_pred = model.predict(X)
    metrics = calculate_metrics(y, y_pred)

    print(f"\n{dataset_name.upper()} Set Metrics:")
    print(f"  MAE:  {metrics['mae']:.3f} years")
    print(f"  RMSE: {metrics['rmse']:.3f} years")
    print(f"  R²:   {metrics['r2']:.3f}")

    return metrics


def compute_age_bio_and_gaps(df: pd.DataFrame,
                             predictions: Dict[str, np.ndarray],
                             age_col: str = 'AGE') -> pd.DataFrame:
    """
    Compute biological ages and age gaps for each organ.

    Args:
        df: DataFrame containing SEQN and chronological age.
        predictions: Dictionary mapping organ names to predicted age arrays.
        age_col: Name of the chronological age column.

    Returns:
        DataFrame with added columns for biological ages and age gaps.

    Example:
        >>> predictions = {
        ...     'liver': np.array([27, 36, 48]),
        ...     'kidney': np.array([24, 33, 43])
        ... }
        >>> result = compute_age_bio_and_gaps(df, predictions)
        >>> print(result[['AGE', 'liver_age_bio', 'liver_age_gap']])
    """
    result_df = df.copy()

    for organ_name, pred_ages in predictions.items():
        # Ensure prediction array matches DataFrame length
        if len(pred_ages) != len(result_df):
            raise ValueError(
                f"Length mismatch: {organ_name} predictions ({len(pred_ages)}) "
                f"vs DataFrame ({len(result_df)})"
            )

        # Add biological age
        bio_age_col = f"{organ_name}_age_bio"
        result_df[bio_age_col] = pred_ages

        # Add age gap (biological age - chronological age)
        gap_col = f"{organ_name}_age_gap"
        result_df[gap_col] = pred_ages - result_df[age_col]

    return result_df


def compare_models(models_metrics: Dict[str, Dict[str, float]],
                  metric: str = 'mae') -> pd.DataFrame:
    """
    Compare performance of multiple models.

    Args:
        models_metrics: Nested dictionary of {model_name: {metric: value}}.
        metric: Primary metric to sort by (default: 'mae').

    Returns:
        DataFrame with model comparison, sorted by specified metric.

    Example:
        >>> metrics = {
        ...     'liver_linear': {'mae': 5.2, 'rmse': 6.8, 'r2': 0.75},
        ...     'liver_nonlinear': {'mae': 3.8, 'rmse': 5.1, 'r2': 0.85}
        ... }
        >>> comparison = compare_models(metrics)
    """
    comparison_data = []

    for model_name, metrics in models_metrics.items():
        row = {'model_name': model_name}
        row.update(metrics)
        comparison_data.append(row)

    comparison_df = pd.DataFrame(comparison_data)

    # Sort by metric (ascending for error metrics, descending for R²)
    ascending = (metric != 'r2')
    if metric in comparison_df.columns:
        comparison_df = comparison_df.sort_values(metric, ascending=ascending)

    return comparison_df


def evaluate_all_organs(models_dict: Dict[str, Dict[str, Any]],
                       splits_dict: Dict[str, Dict],
                       dataset: str = 'test') -> pd.DataFrame:
    """
    Evaluate all organ models on specified dataset.

    Args:
        models_dict: Dictionary of {organ_name: {model_type: model}}.
        splits_dict: Dictionary of {organ_name: {split_name: data}}.
        dataset: Which dataset to evaluate on ('train', 'val', 'test').

    Returns:
        DataFrame with evaluation results for all organs and models.

    Example:
        >>> results = evaluate_all_organs(models_dict, splits_dict, dataset='test')
    """
    all_metrics = {}

    for organ_name, models in models_dict.items():
        print(f"\n{'='*60}")
        print(f"Evaluating {organ_name.upper()}")
        print('='*60)

        splits = splits_dict[organ_name]
        X = splits[f'X_{dataset}']
        y = splits[f'y_{dataset}']

        for model_type, model in models.items():
            model_key = f"{organ_name}_{model_type}"
            metrics = evaluate_model(model, X, y, dataset_name=f"{organ_name} {model_type} {dataset}")
            all_metrics[model_key] = metrics

    # Create comparison DataFrame
    comparison = compare_models(all_metrics)

    print(f"\n{'='*60}")
    print(f"SUMMARY: {dataset.upper()} Set Performance")
    print('='*60)
    print(comparison.to_string(index=False))

    return comparison


def cross_validate_organ_clock(X: pd.DataFrame,
                               y: pd.Series,
                               model_func: callable,
                               n_folds: int = 5) -> Dict[str, float]:
    """
    Perform cross-validation for an organ clock model.

    Args:
        X: Feature matrix.
        y: Target vector.
        model_func: Function that returns an untrained model.
        n_folds: Number of cross-validation folds.

    Returns:
        Dictionary with mean and std of metrics across folds.

    Example:
        >>> from sklearn.linear_model import LinearRegression
        >>> results = cross_validate_organ_clock(X, y, lambda: LinearRegression())
    """
    from sklearn.model_selection import KFold

    kf = KFold(n_splits=n_folds, shuffle=True, random_state=42)

    fold_metrics = {'mae': [], 'rmse': [], 'r2': []}

    for fold_idx, (train_idx, val_idx) in enumerate(kf.split(X), 1):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]

        model = model_func()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_val)
        metrics = calculate_metrics(y_val, y_pred)

        for metric_name, value in metrics.items():
            fold_metrics[metric_name].append(value)

    # Calculate mean and std
    cv_results = {}
    for metric_name, values in fold_metrics.items():
        cv_results[f'{metric_name}_mean'] = np.mean(values)
        cv_results[f'{metric_name}_std'] = np.std(values)

    return cv_results
