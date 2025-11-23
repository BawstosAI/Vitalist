"""
Data preprocessing utilities for NHANES data.

This module provides functions for cleaning, filtering, and encoding NHANES data.
"""

import pandas as pd
import numpy as np
from typing import List, Optional
from sklearn.impute import SimpleImputer


def filter_by_age(df: pd.DataFrame, min_age: int = 18, max_age: int = 80,
                  age_col: str = 'AGE') -> pd.DataFrame:
    """
    Filter dataset by age range.

    Args:
        df: Input DataFrame.
        min_age: Minimum age threshold (inclusive).
        max_age: Maximum age threshold (inclusive).
        age_col: Name of the age column.

    Returns:
        Filtered DataFrame.

    Example:
        >>> df = pd.DataFrame({'AGE': [15, 25, 45, 85]})
        >>> filtered = filter_by_age(df, min_age=18, max_age=80)
        >>> print(len(filtered))
        2
    """
    if age_col not in df.columns:
        raise ValueError(f"Age column '{age_col}' not found in DataFrame")

    initial_count = len(df)
    filtered_df = df[(df[age_col] >= min_age) & (df[age_col] <= max_age)].copy()
    final_count = len(filtered_df)

    print(f"Age filtering: {initial_count} → {final_count} rows "
          f"({initial_count - final_count} removed)")

    return filtered_df


def handle_missing_values(df: pd.DataFrame,
                          missing_threshold: float = 0.5,
                          strategy: str = 'median',
                          numeric_only: bool = True) -> pd.DataFrame:
    """
    Handle missing values in the dataset.

    Strategy:
    1. Drop columns with missing rate > threshold
    2. Impute remaining missing values using specified strategy

    Args:
        df: Input DataFrame.
        missing_threshold: Drop columns with missing rate above this threshold (0-1).
        strategy: Imputation strategy ('mean', 'median', 'most_frequent').
        numeric_only: If True, only process numeric columns.

    Returns:
        DataFrame with missing values handled.

    Example:
        >>> df = pd.DataFrame({'A': [1, 2, np.nan], 'B': [np.nan, np.nan, np.nan]})
        >>> clean = handle_missing_values(df, missing_threshold=0.5)
    """
    df_clean = df.copy()
    initial_shape = df_clean.shape

    # Calculate missing rates
    missing_rates = df_clean.isnull().mean()
    print("\nMissing value analysis:")
    print(f"Columns with >10% missing: {(missing_rates > 0.1).sum()}")

    # Drop columns with high missing rate
    cols_to_drop = missing_rates[missing_rates > missing_threshold].index.tolist()
    if cols_to_drop:
        print(f"Dropping {len(cols_to_drop)} columns with >{missing_threshold*100}% missing")
        df_clean = df_clean.drop(columns=cols_to_drop)

    # Impute remaining missing values in numeric columns
    if numeric_only:
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        imputer = SimpleImputer(strategy=strategy)

        if len(numeric_cols) > 0:
            df_clean[numeric_cols] = imputer.fit_transform(df_clean[numeric_cols])
            print(f"Imputed missing values in {len(numeric_cols)} numeric columns using '{strategy}' strategy")

    final_shape = df_clean.shape
    print(f"Shape after handling missing values: {initial_shape} → {final_shape}")

    return df_clean


def encode_categorical_variables(df: pd.DataFrame,
                                 categorical_cols: Optional[List[str]] = None,
                                 drop_first: bool = True) -> pd.DataFrame:
    """
    Encode categorical variables using one-hot encoding.

    Args:
        df: Input DataFrame.
        categorical_cols: List of categorical column names to encode.
                         If None, auto-detects object/category dtypes.
        drop_first: If True, drop first dummy to avoid multicollinearity.

    Returns:
        DataFrame with categorical variables encoded.

    Example:
        >>> df = pd.DataFrame({'SEX': ['Male', 'Female', 'Male'], 'AGE': [25, 35, 45]})
        >>> encoded = encode_categorical_variables(df, categorical_cols=['SEX'])
    """
    df_encoded = df.copy()

    # Auto-detect categorical columns if not specified
    if categorical_cols is None:
        categorical_cols = df_encoded.select_dtypes(include=['object', 'category']).columns.tolist()

    if not categorical_cols:
        print("No categorical columns to encode")
        return df_encoded

    print(f"\nEncoding {len(categorical_cols)} categorical variables:")
    for col in categorical_cols:
        print(f"  - {col}: {df_encoded[col].nunique()} unique values")

    # One-hot encode
    df_encoded = pd.get_dummies(
        df_encoded,
        columns=categorical_cols,
        drop_first=drop_first,
        dtype=int
    )

    print(f"Shape after encoding: {df.shape} → {df_encoded.shape}")

    return df_encoded


def remove_outliers(df: pd.DataFrame,
                   columns: List[str],
                   method: str = 'iqr',
                   threshold: float = 3.0) -> pd.DataFrame:
    """
    Remove outliers from specified columns.

    Args:
        df: Input DataFrame.
        columns: List of column names to check for outliers.
        method: Method to use ('iqr' or 'zscore').
        threshold: Threshold for outlier detection (IQR multiplier or z-score).

    Returns:
        DataFrame with outliers removed.

    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 3, 100]})
        >>> clean = remove_outliers(df, columns=['A'], method='iqr')
    """
    df_clean = df.copy()
    initial_count = len(df_clean)

    for col in columns:
        if col not in df_clean.columns:
            print(f"Warning: Column '{col}' not found, skipping")
            continue

        if method == 'iqr':
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR

            outliers = (df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)

        elif method == 'zscore':
            z_scores = np.abs((df_clean[col] - df_clean[col].mean()) / df_clean[col].std())
            outliers = z_scores > threshold

        else:
            raise ValueError(f"Unknown method: {method}. Use 'iqr' or 'zscore'.")

        n_outliers = outliers.sum()
        if n_outliers > 0:
            df_clean = df_clean[~outliers]
            print(f"Removed {n_outliers} outliers from '{col}'")

    final_count = len(df_clean)
    print(f"\nTotal rows removed: {initial_count - final_count}")

    return df_clean


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to uppercase and replace spaces with underscores.

    Args:
        df: Input DataFrame.

    Returns:
        DataFrame with standardized column names.
    """
    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.upper().str.replace(' ', '_')
    return df_clean
