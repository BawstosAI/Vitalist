"""
Configuration management for organ aging analysis.

This module handles loading and parsing of YAML configuration files for:
- File paths to NHANES data
- Organ panel definitions (biomarker mappings)
"""

import yaml
from pathlib import Path
from typing import Dict, Any


def load_paths_config(config_path: str = "configs/paths.yaml") -> Dict[str, Any]:
    """
    Load paths configuration from YAML file.

    Args:
        config_path: Path to the paths configuration YAML file.

    Returns:
        Dictionary containing paths configuration.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        yaml.YAMLError: If the YAML file is malformed.

    Example:
        >>> config = load_paths_config("configs/paths.yaml")
        >>> print(config['raw_data_dir'])
        'data/raw'
    """
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    return config


def load_organ_panels_config(config_path: str = "configs/organ_panels.yaml") -> Dict[str, Any]:
    """
    Load organ panels configuration from YAML file.

    This configuration maps organ systems to their corresponding biomarker variables.

    Args:
        config_path: Path to the organ panels configuration YAML file.

    Returns:
        Dictionary mapping organ names to lists of biomarker variable names.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        yaml.YAMLError: If the YAML file is malformed.

    Example:
        >>> panels = load_organ_panels_config("configs/organ_panels.yaml")
        >>> print(panels['liver'])
        ['ALT', 'AST', 'GGT', 'ALBUMIN']
    """
    config_file = Path(config_path)

    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    return config


def get_project_root() -> Path:
    """
    Get the project root directory.

    Returns:
        Path object pointing to the project root.
    """
    # Assumes this file is in src/organ_aging/
    return Path(__file__).parent.parent.parent


def validate_config(config: Dict[str, Any], required_keys: list) -> bool:
    """
    Validate that a configuration dictionary contains required keys.

    Args:
        config: Configuration dictionary to validate.
        required_keys: List of required key names.

    Returns:
        True if all required keys are present.

    Raises:
        ValueError: If any required key is missing.
    """
    missing_keys = [key for key in required_keys if key not in config]

    if missing_keys:
        raise ValueError(f"Missing required configuration keys: {missing_keys}")

    return True
