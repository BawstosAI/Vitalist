"""Tests for config module."""
import pytest
import yaml
from pathlib import Path
from src.organ_aging.config import load_paths_config, load_organ_panels_config


class TestConfigLoading:
    """Test configuration loading functions."""

    def test_load_paths_config_returns_dict(self, tmp_path):
        """Test that load_paths_config returns a dictionary."""
        # Create temporary config file
        config_file = tmp_path / "paths.yaml"
        config_data = {
            "raw_data_dir": "data/raw",
            "nhanes_files": {
                "demographics": "DEMO.XPT",
                "biochemistry": "BIOPRO.XPT"
            }
        }
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)

        result = load_paths_config(str(config_file))
        assert isinstance(result, dict)
        assert "raw_data_dir" in result
        assert "nhanes_files" in result

    def test_load_organ_panels_config_returns_dict(self, tmp_path):
        """Test that load_organ_panels_config returns a dictionary."""
        config_file = tmp_path / "organ_panels.yaml"
        config_data = {
            "liver": ["ALT", "AST", "GGT"],
            "kidney": ["CREATININE", "BUN"],
            "global_covariates": ["AGE", "SEX", "BMI"]
        }
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)

        result = load_organ_panels_config(str(config_file))
        assert isinstance(result, dict)
        assert "liver" in result
        assert "kidney" in result
        assert isinstance(result["liver"], list)

    def test_load_paths_config_raises_on_missing_file(self):
        """Test that loading nonexistent config raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_paths_config("nonexistent.yaml")
