"""Tests for evaluation module."""
import pytest
import pandas as pd
import numpy as np
from src.organ_aging.evaluation import (
    calculate_metrics,
    compute_age_bio_and_gaps,
    compare_models
)


class TestEvaluation:
    """Test model evaluation functions."""

    def test_calculate_metrics_returns_dict(self):
        """Test metrics calculation."""
        y_true = np.array([25, 35, 45, 55, 65])
        y_pred = np.array([26, 34, 46, 54, 66])

        metrics = calculate_metrics(y_true, y_pred)
        assert isinstance(metrics, dict)
        assert 'mae' in metrics
        assert 'rmse' in metrics
        assert 'r2' in metrics
        assert metrics['mae'] >= 0
        assert metrics['r2'] <= 1.0

    def test_compute_age_bio_and_gaps_creates_correct_columns(self):
        """Test age gap computation."""
        df = pd.DataFrame({
            'SEQN': [1, 2, 3, 4, 5],
            'AGE': [25, 35, 45, 55, 65]
        })

        predictions = {
            'liver': np.array([27, 36, 48, 53, 67]),
            'kidney': np.array([24, 33, 43, 56, 66])
        }

        result = compute_age_bio_and_gaps(df, predictions)
        assert 'liver_age_bio' in result.columns
        assert 'liver_age_gap' in result.columns
        assert 'kidney_age_bio' in result.columns
        assert 'kidney_age_gap' in result.columns

        # Check gap calculation
        assert result.loc[0, 'liver_age_gap'] == pytest.approx(2.0)  # 27 - 25
        assert result.loc[0, 'kidney_age_gap'] == pytest.approx(-1.0)  # 24 - 25

    def test_compare_models_returns_comparison_df(self):
        """Test model comparison."""
        models_metrics = {
            'liver_linear': {'mae': 5.2, 'rmse': 6.8, 'r2': 0.75},
            'liver_nonlinear': {'mae': 3.8, 'rmse': 5.1, 'r2': 0.85},
            'kidney_linear': {'mae': 4.9, 'rmse': 6.3, 'r2': 0.78}
        }

        result = compare_models(models_metrics)
        assert isinstance(result, pd.DataFrame)
        assert 'model_name' in result.columns
        assert 'mae' in result.columns
        assert len(result) == 3
