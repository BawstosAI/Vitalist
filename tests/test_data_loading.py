"""Tests for data loading module."""
import pytest
import pandas as pd
import numpy as np
from src.organ_aging.data_loading import load_nhanes_tables, merge_nhanes_tables


class TestDataLoading:
    """Test NHANES data loading functions."""

    def test_load_nhanes_tables_returns_dict_of_dataframes(self, tmp_path):
        """Test that load_nhanes_tables returns dict of DataFrames."""
        # Create mock CSV files
        demo_file = tmp_path / "DEMO.csv"
        bio_file = tmp_path / "BIOPRO.csv"

        pd.DataFrame({
            'SEQN': [1, 2, 3],
            'AGE': [25, 35, 45],
            'SEX': [1, 2, 1]
        }).to_csv(demo_file, index=False)

        pd.DataFrame({
            'SEQN': [1, 2, 3],
            'ALT': [20, 25, 30],
            'AST': [18, 22, 28]
        }).to_csv(bio_file, index=False)

        paths_config = {
            "raw_data_dir": str(tmp_path),
            "nhanes_files": {
                "demographics": "DEMO.csv",
                "biochemistry": "BIOPRO.csv"
            }
        }

        result = load_nhanes_tables(paths_config)
        assert isinstance(result, dict)
        assert "demographics" in result
        assert "biochemistry" in result
        assert isinstance(result["demographics"], pd.DataFrame)

    def test_merge_nhanes_tables_merges_on_seqn(self):
        """Test that merge_nhanes_tables properly merges on SEQN."""
        tables = {
            "demographics": pd.DataFrame({
                'SEQN': [1, 2, 3],
                'AGE': [25, 35, 45]
            }),
            "biochemistry": pd.DataFrame({
                'SEQN': [1, 2, 3],
                'ALT': [20, 25, 30]
            })
        }

        result = merge_nhanes_tables(tables)
        assert isinstance(result, pd.DataFrame)
        assert 'SEQN' in result.columns
        assert 'AGE' in result.columns
        assert 'ALT' in result.columns
        assert len(result) == 3

    def test_merge_nhanes_tables_handles_missing_seqn(self):
        """Test that merge handles non-overlapping SEQN values."""
        tables = {
            "demographics": pd.DataFrame({
                'SEQN': [1, 2, 3],
                'AGE': [25, 35, 45]
            }),
            "biochemistry": pd.DataFrame({
                'SEQN': [2, 3, 4],
                'ALT': [25, 30, 35]
            })
        }

        result = merge_nhanes_tables(tables)
        assert isinstance(result, pd.DataFrame)
        # Inner join should only have overlapping SEQN
        assert len(result) >= 2
