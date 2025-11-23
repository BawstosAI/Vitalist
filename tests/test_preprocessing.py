"""Tests for preprocessing module."""
import pytest
import pandas as pd
import numpy as np
from src.organ_aging.preprocessing import (
    filter_by_age,
    handle_missing_values,
    encode_categorical_variables
)


class TestPreprocessing:
    """Test data preprocessing functions."""

    def test_filter_by_age_filters_correctly(self):
        """Test age filtering."""
        df = pd.DataFrame({
            'SEQN': [1, 2, 3, 4, 5],
            'AGE': [15, 25, 45, 65, 85]
        })

        result = filter_by_age(df, min_age=18, max_age=80)
        assert len(result) == 3
        assert result['AGE'].min() >= 18
        assert result['AGE'].max() <= 80

    def test_handle_missing_values_drops_high_missing(self):
        """Test that columns with high missing rate are dropped."""
        df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [1, np.nan, np.nan, np.nan, np.nan],  # 80% missing
            'C': [1, 2, np.nan, 4, 5]  # 20% missing
        })

        result = handle_missing_values(df, missing_threshold=0.5)
        assert 'A' in result.columns
        assert 'B' not in result.columns
        assert 'C' in result.columns

    def test_encode_categorical_variables_creates_dummies(self):
        """Test categorical encoding."""
        df = pd.DataFrame({
            'SEQN': [1, 2, 3],
            'SEX': ['Male', 'Female', 'Male'],
            'AGE': [25, 35, 45]
        })

        result = encode_categorical_variables(df, categorical_cols=['SEX'])
        assert 'SEX_Male' in result.columns or 'SEX_Female' in result.columns
        assert 'AGE' in result.columns

    def test_handle_missing_values_imputes_numeric(self):
        """Test that numeric missing values are imputed."""
        df = pd.DataFrame({
            'A': [1.0, 2.0, np.nan, 4.0, 5.0],
            'B': [10.0, 20.0, 30.0, 40.0, 50.0]
        })

        result = handle_missing_values(df, strategy='median')
        assert not result['A'].isna().any()
        assert result['A'].median() > 0
