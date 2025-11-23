"""Tests for models module."""
import pytest
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from src.organ_aging.models import (
    train_linear_model,
    train_nonlinear_model,
    save_model,
    load_model
)


class TestModels:
    """Test model training functions."""

    def test_train_linear_model_returns_fitted_model(self):
        """Test linear model training."""
        X_train = pd.DataFrame({
            'feature1': np.random.randn(50),
            'feature2': np.random.randn(50)
        })
        y_train = pd.Series(np.random.randint(20, 80, 50))

        model = train_linear_model(X_train, y_train)
        assert model is not None
        assert hasattr(model, 'predict')

        # Test prediction
        predictions = model.predict(X_train)
        assert len(predictions) == len(y_train)

    def test_train_nonlinear_model_returns_fitted_model(self):
        """Test non-linear model training."""
        X_train = pd.DataFrame({
            'feature1': np.random.randn(50),
            'feature2': np.random.randn(50)
        })
        y_train = pd.Series(np.random.randint(20, 80, 50))

        model = train_nonlinear_model(X_train, y_train, model_type='hist_gb')
        assert model is not None
        assert hasattr(model, 'predict')

        predictions = model.predict(X_train)
        assert len(predictions) == len(y_train)

    def test_save_and_load_model(self, tmp_path):
        """Test model saving and loading."""
        X_train = pd.DataFrame({
            'feature1': np.random.randn(50),
            'feature2': np.random.randn(50)
        })
        y_train = pd.Series(np.random.randint(20, 80, 50))

        model = train_linear_model(X_train, y_train)
        model_path = tmp_path / "test_model.pkl"

        save_model(model, str(model_path))
        loaded_model = load_model(str(model_path))

        assert loaded_model is not None
        original_pred = model.predict(X_train)
        loaded_pred = loaded_model.predict(X_train)
        np.testing.assert_array_almost_equal(original_pred, loaded_pred)
