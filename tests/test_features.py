"""Tests for feature engineering module."""
import pytest
import pandas as pd
import numpy as np
from src.organ_aging.features import (
    build_organ_datasets,
    split_train_val_test,
    scale_features
)


class TestFeatureEngineering:
    """Test feature engineering functions."""

    def test_build_organ_datasets_creates_datasets_per_organ(self):
        """Test that datasets are created for each organ panel."""
        df = pd.DataFrame({
            'SEQN': [1, 2, 3, 4, 5],
            'AGE': [25, 35, 45, 55, 65],
            'ALT': [20, 25, 30, 35, 40],
            'AST': [18, 22, 28, 32, 38],
            'SEX': [1, 2, 1, 2, 1],
            'BMI': [22, 25, 28, 30, 26]
        })

        organ_panels = {
            'liver': ['ALT', 'AST'],
            'global_covariates': ['SEX', 'BMI']
        }

        result = build_organ_datasets(df, organ_panels, global_covars=['SEX', 'BMI'])
        assert isinstance(result, dict)
        assert 'liver' in result
        X, y = result['liver']
        assert isinstance(X, pd.DataFrame)
        assert isinstance(y, pd.Series)
        assert 'ALT' in X.columns
        assert 'SEX' in X.columns
        assert len(y) == len(df)

    def test_split_train_val_test_splits_correctly(self):
        """Test train/val/test split."""
        X = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100)
        })
        y = pd.Series(np.random.randint(20, 80, 100))

        result = split_train_val_test(X, y, train_size=0.6, val_size=0.2, random_state=42)
        X_train, X_val, X_test, y_train, y_val, y_test = result

        assert len(X_train) == 60
        assert len(X_val) == 20
        assert len(X_test) == 20
        assert len(y_train) == 60

    def test_scale_features_returns_scaled_data(self):
        """Test feature scaling."""
        X_train = pd.DataFrame({
            'feature1': [1, 2, 3, 4, 5],
            'feature2': [10, 20, 30, 40, 50]
        })
        X_test = pd.DataFrame({
            'feature1': [2, 3],
            'feature2': [20, 30]
        })

        X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test)

        assert X_train_scaled.shape == X_train.shape
        assert X_test_scaled.shape == X_test.shape
        assert abs(X_train_scaled.mean().mean()) < 0.1  # Close to 0
        assert scaler is not None
