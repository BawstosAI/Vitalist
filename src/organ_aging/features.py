"""
Feature engineering for organ-specific datasets.

This module handles construction of organ-specific feature matrices,
train/val/test splitting, and feature scaling.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, RobustScaler


def build_organ_datasets(df: pd.DataFrame,
                        organ_panels: Dict[str, List[str]],
                        global_covars: List[str],
                        target_col: str = 'AGE') -> Dict[str, Tuple[pd.DataFrame, pd.Series]]:
    """
    Build organ-specific datasets by combining organ biomarkers with global covariates.

    Args:
        df: Input DataFrame containing all biomarkers and covariates.
        organ_panels: Dictionary mapping organ names to lists of biomarker column names.
        global_covars: List of global covariate columns (e.g., SEX, BMI, SMOKING_STATUS).
        target_col: Name of the target variable (chronological age).

    Returns:
        Dictionary mapping organ names to tuples of (X, y) where:
        - X is the feature matrix (biomarkers + global covariates)
        - y is the target vector (chronological age)

    Example:
        >>> organ_panels = {'liver': ['ALT', 'AST'], 'global_covariates': ['SEX', 'BMI']}
        >>> datasets = build_organ_datasets(df, organ_panels, global_covars=['SEX', 'BMI'])
        >>> X_liver, y_liver = datasets['liver']
    """
    if target_col not in df.columns:
        raise ValueError(f"Target column '{target_col}' not found in DataFrame")

    # Remove 'global_covariates' from organ panels if present
    organ_names = [name for name in organ_panels.keys() if name != 'global_covariates']

    organ_datasets = {}

    for organ_name in organ_names:
        biomarkers = organ_panels[organ_name]

        # Check which biomarkers are available
        available_biomarkers = [col for col in biomarkers if col in df.columns]
        missing_biomarkers = set(biomarkers) - set(available_biomarkers)

        if missing_biomarkers:
            print(f"Warning: {organ_name} - missing biomarkers: {missing_biomarkers}")

        if not available_biomarkers:
            print(f"Warning: {organ_name} - no biomarkers available, skipping")
            continue

        # Combine organ biomarkers with global covariates
        feature_cols = available_biomarkers + [col for col in global_covars if col in df.columns]

        # Remove duplicates while preserving order
        feature_cols = list(dict.fromkeys(feature_cols))

        # Extract features and target
        X = df[feature_cols].copy()
        y = df[target_col].copy()

        # Drop rows with any missing values
        valid_idx = X.notna().all(axis=1) & y.notna()
        X = X[valid_idx]
        y = y[valid_idx]

        organ_datasets[organ_name] = (X, y)

        print(f"{organ_name}: {X.shape[0]} samples, {X.shape[1]} features "
              f"({len(available_biomarkers)} biomarkers + {len(feature_cols) - len(available_biomarkers)} covariates)")

    return organ_datasets


def split_train_val_test(X: pd.DataFrame,
                         y: pd.Series,
                         train_size: float = 0.6,
                         val_size: float = 0.2,
                         random_state: int = 42,
                         stratify_bins: Optional[int] = None) -> Tuple:
    """
    Split data into train, validation, and test sets.

    Args:
        X: Feature matrix.
        y: Target vector.
        train_size: Proportion for training set (default 0.6).
        val_size: Proportion for validation set (default 0.2).
                 Test set gets the remainder (1 - train_size - val_size).
        random_state: Random seed for reproducibility.
        stratify_bins: If provided, stratify split by age bins (number of bins).

    Returns:
        Tuple of (X_train, X_val, X_test, y_train, y_val, y_test).

    Example:
        >>> X_train, X_val, X_test, y_train, y_val, y_test = split_train_val_test(X, y)
    """
    test_size = 1 - train_size - val_size
    if test_size < 0:
        raise ValueError("train_size + val_size must be <= 1")

    # Optionally stratify by age bins
    stratify = None
    if stratify_bins:
        age_bins = pd.cut(y, bins=stratify_bins, labels=False)
        stratify = age_bins

    # First split: train + val vs test
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify
    )

    # Second split: train vs val
    val_size_adjusted = val_size / (train_size + val_size)

    if stratify_bins:
        stratify_temp = pd.cut(y_temp, bins=stratify_bins, labels=False)
    else:
        stratify_temp = None

    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp,
        test_size=val_size_adjusted,
        random_state=random_state,
        stratify=stratify_temp
    )

    print(f"Split sizes - Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")

    return X_train, X_val, X_test, y_train, y_val, y_test


def scale_features(X_train: pd.DataFrame,
                  X_val: Optional[pd.DataFrame] = None,
                  X_test: Optional[pd.DataFrame] = None,
                  method: str = 'standard') -> Tuple:
    """
    Scale features using StandardScaler or RobustScaler.

    Fits scaler on training data and transforms all sets.

    Args:
        X_train: Training feature matrix.
        X_val: Validation feature matrix (optional).
        X_test: Test feature matrix (optional).
        method: Scaling method ('standard' or 'robust').

    Returns:
        Tuple of (X_train_scaled, X_val_scaled, X_test_scaled, scaler)
        where X_val_scaled and X_test_scaled are None if inputs were None.

    Example:
        >>> X_train_scaled, X_val_scaled, X_test_scaled, scaler = scale_features(
        ...     X_train, X_val, X_test, method='standard'
        ... )
    """
    if method == 'standard':
        scaler = StandardScaler()
    elif method == 'robust':
        scaler = RobustScaler()
    else:
        raise ValueError(f"Unknown scaling method: {method}. Use 'standard' or 'robust'.")

    # Fit on training data
    X_train_scaled = pd.DataFrame(
        scaler.fit_transform(X_train),
        columns=X_train.columns,
        index=X_train.index
    )

    # Transform validation and test sets
    X_val_scaled = None
    X_test_scaled = None

    if X_val is not None:
        X_val_scaled = pd.DataFrame(
            scaler.transform(X_val),
            columns=X_val.columns,
            index=X_val.index
        )

    if X_test is not None:
        X_test_scaled = pd.DataFrame(
            scaler.transform(X_test),
            columns=X_test.columns,
            index=X_test.index
        )

    print(f"Features scaled using {method} scaler")

    return X_train_scaled, X_val_scaled, X_test_scaled, scaler


def select_features_by_variance(X: pd.DataFrame, threshold: float = 0.01) -> List[str]:
    """
    Select features with variance above threshold.

    Args:
        X: Feature matrix.
        threshold: Minimum variance threshold.

    Returns:
        List of selected feature names.

    Example:
        >>> selected = select_features_by_variance(X, threshold=0.01)
    """
    variances = X.var()
    selected = variances[variances > threshold].index.tolist()

    print(f"Selected {len(selected)}/{len(X.columns)} features with variance > {threshold}")

    return selected
