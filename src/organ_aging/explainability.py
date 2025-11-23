"""
Model explainability and interpretability tools.

This module provides functions for explaining organ clock predictions
using feature importance, SHAP values, and other interpretability methods.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Any, Optional, List
import warnings


def get_feature_importance(model: Any,
                          feature_names: List[str],
                          importance_type: str = 'auto') -> pd.DataFrame:
    """
    Extract feature importance from a trained model.

    Args:
        model: Trained model.
        feature_names: List of feature names.
        importance_type: Type of importance ('auto', 'coef', 'gain', 'split').

    Returns:
        DataFrame with feature names and importance scores, sorted by importance.

    Example:
        >>> importance = get_feature_importance(model, X_train.columns.tolist())
        >>> print(importance.head())
    """
    if hasattr(model, 'feature_importances_'):
        # Tree-based models
        importances = model.feature_importances_

    elif hasattr(model, 'coef_'):
        # Linear models - use absolute coefficients
        importances = np.abs(model.coef_)

    else:
        raise ValueError("Model does not have feature_importances_ or coef_ attribute")

    # Create DataFrame
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    })

    # Sort by importance
    importance_df = importance_df.sort_values('importance', ascending=False)

    return importance_df


def plot_feature_importance(importance_df: pd.DataFrame,
                           top_n: int = 20,
                           title: str = "Feature Importance",
                           figsize: tuple = (10, 8)) -> plt.Figure:
    """
    Plot feature importance as a horizontal bar chart.

    Args:
        importance_df: DataFrame with 'feature' and 'importance' columns.
        top_n: Number of top features to display.
        title: Plot title.
        figsize: Figure size.

    Returns:
        Matplotlib figure object.

    Example:
        >>> fig = plot_feature_importance(importance_df, top_n=15)
        >>> plt.show()
    """
    top_features = importance_df.head(top_n)

    fig, ax = plt.subplots(figsize=figsize)

    ax.barh(range(len(top_features)), top_features['importance'])
    ax.set_yticks(range(len(top_features)))
    ax.set_yticklabels(top_features['feature'])
    ax.set_xlabel('Importance')
    ax.set_title(title)
    ax.invert_yaxis()

    plt.tight_layout()

    return fig


def calculate_shap_values(model: Any,
                         X: pd.DataFrame,
                         background_samples: Optional[int] = 100) -> Any:
    """
    Calculate SHAP values for model predictions.

    Requires the 'shap' package to be installed.

    Args:
        model: Trained model.
        X: Feature matrix to explain.
        background_samples: Number of background samples for TreeExplainer.

    Returns:
        SHAP Explanation object.

    Example:
        >>> # Requires: pip install shap
        >>> shap_values = calculate_shap_values(model, X_test)
        >>> shap.summary_plot(shap_values, X_test)

    Note:
        If SHAP is not installed, this function will raise an ImportError
        with installation instructions.
    """
    try:
        import shap
    except ImportError:
        raise ImportError(
            "SHAP package not installed. Install with: pip install shap\n"
            "For faster tree-based explanations, also install: pip install shap[tree]"
        )

    # Choose appropriate explainer based on model type
    if hasattr(model, 'tree_'):
        # Single tree models
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X)

    elif hasattr(model, 'estimators_'):
        # Ensemble tree models (XGBoost, LightGBM, HistGradientBoosting)
        if background_samples and len(X) > background_samples:
            background = shap.sample(X, background_samples)
            explainer = shap.TreeExplainer(model, background)
        else:
            explainer = shap.TreeExplainer(model)

        shap_values = explainer.shap_values(X)

    elif hasattr(model, 'coef_'):
        # Linear models
        explainer = shap.LinearExplainer(model, X)
        shap_values = explainer.shap_values(X)

    else:
        # Fallback to KernelExplainer (slower)
        warnings.warn("Using KernelExplainer - this may be slow for large datasets")
        if background_samples and len(X) > background_samples:
            background = shap.sample(X, background_samples)
        else:
            background = X

        explainer = shap.KernelExplainer(model.predict, background)
        shap_values = explainer.shap_values(X)

    return shap.Explanation(
        values=shap_values,
        base_values=explainer.expected_value if hasattr(explainer, 'expected_value') else None,
        data=X.values,
        feature_names=X.columns.tolist()
    )


def plot_shap_summary(shap_explanation: Any,
                     X: pd.DataFrame,
                     plot_type: str = 'dot',
                     max_display: int = 20) -> None:
    """
    Create SHAP summary plot.

    Args:
        shap_explanation: SHAP Explanation object.
        X: Feature matrix.
        plot_type: Type of plot ('dot', 'bar', 'violin').
        max_display: Maximum number of features to display.

    Example:
        >>> shap_exp = calculate_shap_values(model, X_test)
        >>> plot_shap_summary(shap_exp, X_test, plot_type='dot')
    """
    try:
        import shap
    except ImportError:
        raise ImportError("SHAP package not installed. Install with: pip install shap")

    if plot_type == 'dot':
        shap.summary_plot(shap_explanation, X, max_display=max_display)
    elif plot_type == 'bar':
        shap.summary_plot(shap_explanation, X, plot_type='bar', max_display=max_display)
    elif plot_type == 'violin':
        shap.summary_plot(shap_explanation, X, plot_type='violin', max_display=max_display)
    else:
        raise ValueError(f"Unknown plot_type: {plot_type}")


def calculate_permutation_importance(model: Any,
                                    X: pd.DataFrame,
                                    y: pd.Series,
                                    n_repeats: int = 10,
                                    random_state: int = 42) -> pd.DataFrame:
    """
    Calculate permutation importance for model features.

    This is a model-agnostic method that works with any model.

    Args:
        model: Trained model.
        X: Feature matrix.
        y: Target vector.
        n_repeats: Number of times to permute each feature.
        random_state: Random seed.

    Returns:
        DataFrame with feature names, importance mean, and std.

    Example:
        >>> perm_importance = calculate_permutation_importance(model, X_test, y_test)
        >>> print(perm_importance.head())
    """
    from sklearn.inspection import permutation_importance

    result = permutation_importance(
        model, X, y,
        n_repeats=n_repeats,
        random_state=random_state,
        n_jobs=-1
    )

    importance_df = pd.DataFrame({
        'feature': X.columns,
        'importance_mean': result.importances_mean,
        'importance_std': result.importances_std
    })

    importance_df = importance_df.sort_values('importance_mean', ascending=False)

    return importance_df


def analyze_prediction_errors(y_true: np.ndarray,
                             y_pred: np.ndarray,
                             X: Optional[pd.DataFrame] = None,
                             threshold_percentile: float = 90) -> pd.DataFrame:
    """
    Analyze prediction errors to identify patterns.

    Args:
        y_true: True age values.
        y_pred: Predicted age values.
        X: Optional feature matrix to include in analysis.
        threshold_percentile: Percentile threshold for large errors.

    Returns:
        DataFrame with error analysis.

    Example:
        >>> error_analysis = analyze_prediction_errors(y_test, predictions, X_test)
    """
    errors = y_pred - y_true
    abs_errors = np.abs(errors)

    analysis_df = pd.DataFrame({
        'y_true': y_true,
        'y_pred': y_pred,
        'error': errors,
        'abs_error': abs_errors
    })

    # Add feature values if provided
    if X is not None:
        for col in X.columns:
            analysis_df[col] = X[col].values

    # Flag large errors
    threshold = np.percentile(abs_errors, threshold_percentile)
    analysis_df['large_error'] = abs_errors > threshold

    print(f"\nError Analysis:")
    print(f"  Mean error: {errors.mean():.3f} years")
    print(f"  Mean absolute error: {abs_errors.mean():.3f} years")
    print(f"  Large errors (>{threshold_percentile}th percentile): {analysis_df['large_error'].sum()}")

    return analysis_df
