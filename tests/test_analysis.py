"""Tests for analysis module."""
import pytest
import pandas as pd
import numpy as np
from src.organ_aging.analysis import (
    bin_by_age,
    calculate_gap_correlations,
    identify_advanced_organs,
    analyze_cooccurrence
)


class TestAnalysis:
    """Test analysis functions."""

    def test_bin_by_age_creates_bins(self):
        """Test age binning."""
        df = pd.DataFrame({
            'AGE': [20, 25, 35, 45, 55, 65, 75]
        })

        result = bin_by_age(df, bins=[18, 30, 40, 50, 60, 70, 80])
        assert 'age_bin' in result.columns
        assert result['age_bin'].nunique() <= 6

    def test_calculate_gap_correlations_returns_correlation_matrix(self):
        """Test gap correlation calculation."""
        df = pd.DataFrame({
            'liver_age_gap': np.random.randn(50),
            'kidney_age_gap': np.random.randn(50),
            'cardio_age_gap': np.random.randn(50)
        })

        result = calculate_gap_correlations(df)
        assert isinstance(result, pd.DataFrame)
        assert result.shape[0] == result.shape[1]  # Square matrix
        assert 'liver_age_gap' in result.columns

    def test_identify_advanced_organs_flags_correctly(self):
        """Test identification of advanced organs."""
        df = pd.DataFrame({
            'SEQN': [1, 2, 3, 4],
            'liver_age_gap': [2, -1, 8, 3],
            'kidney_age_gap': [-2, 6, 1, 7]
        })

        result = identify_advanced_organs(df, threshold=5)
        assert 'liver_advanced' in result.columns
        assert 'kidney_advanced' in result.columns
        assert result.loc[2, 'liver_advanced'] == True  # gap = 8 > 5
        assert result.loc[0, 'liver_advanced'] == False  # gap = 2 < 5

    def test_analyze_cooccurrence_counts_combinations(self):
        """Test co-occurrence analysis."""
        df = pd.DataFrame({
            'SEQN': [1, 2, 3, 4],
            'liver_advanced': [True, False, True, True],
            'kidney_advanced': [False, True, True, False]
        })

        result = analyze_cooccurrence(df, organ_cols=['liver_advanced', 'kidney_advanced'])
        assert isinstance(result, dict)
        assert 'both' in result or 'counts' in result
