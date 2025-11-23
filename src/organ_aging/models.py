"""
Model training and management for organ clocks.

This module provides functions for training linear and non-linear models,
as well as saving and loading trained models.
"""

import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import Any, Optional, Dict
from sklearn.linear_model import LinearRegression, ElasticNet
from sklearn.ensemble import HistGradientBoostingRegressor
import warnings


def train_linear_model(X_train: pd.DataFrame,
                      y_train: pd.Series,
                      model_type: str = 'linear',
                      **kwargs) -> Any:
    """
    Train a linear model for age prediction.

    Args:
        X_train: Training feature matrix.
        y_train: Training target vector.
        model_type: Type of linear model ('linear' or 'elastic_net').
        **kwargs: Additional parameters for the model.

    Returns:
        Fitted model object.

    Example:
        >>> model = train_linear_model(X_train, y_train, model_type='linear')
        >>> predictions = model.predict(X_test)
    """
    if model_type == 'linear':
        model = LinearRegression(**kwargs)
    elif model_type == 'elastic_net':
        # Default ElasticNet parameters if not provided
        default_params = {'alpha': 0.1, 'l1_ratio': 0.5, 'random_state': 42}
        default_params.update(kwargs)
        model = ElasticNet(**default_params)
    else:
        raise ValueError(f"Unknown linear model type: {model_type}")

    print(f"Training {model_type} model...")
    model.fit(X_train, y_train)

    return model


def train_nonlinear_model(X_train: pd.DataFrame,
                         y_train: pd.Series,
                         model_type: str = 'hist_gb',
                         **kwargs) -> Any:
    """
    Train a non-linear model for age prediction.

    Args:
        X_train: Training feature matrix.
        y_train: Training target vector.
        model_type: Type of non-linear model ('hist_gb', 'xgboost', 'lightgbm').
        **kwargs: Additional parameters for the model.

    Returns:
        Fitted model object.

    Example:
        >>> model = train_nonlinear_model(X_train, y_train, model_type='hist_gb')
        >>> predictions = model.predict(X_test)
    """
    if model_type == 'hist_gb':
        # Default HistGradientBoosting parameters
        default_params = {
            'max_iter': 100,
            'max_depth': 10,
            'learning_rate': 0.1,
            'random_state': 42
        }
        default_params.update(kwargs)
        model = HistGradientBoostingRegressor(**default_params)

    elif model_type == 'xgboost':
        try:
            import xgboost as xgb
            default_params = {
                'n_estimators': 100,
                'max_depth': 6,
                'learning_rate': 0.1,
                'random_state': 42
            }
            default_params.update(kwargs)
            model = xgb.XGBRegressor(**default_params)
        except ImportError:
            raise ImportError("XGBoost not installed. Install with: pip install xgboost")

    elif model_type == 'lightgbm':
        try:
            import lightgbm as lgb
            default_params = {
                'n_estimators': 100,
                'max_depth': 10,
                'learning_rate': 0.1,
                'random_state': 42,
                'verbose': -1
            }
            default_params.update(kwargs)
            model = lgb.LGBMRegressor(**default_params)
        except ImportError:
            raise ImportError("LightGBM not installed. Install with: pip install lightgbm")

    else:
        raise ValueError(f"Unknown non-linear model type: {model_type}")

    print(f"Training {model_type} model...")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model.fit(X_train, y_train)

    return model


def save_model(model: Any, filepath: str, metadata: Optional[Dict] = None) -> None:
    """
    Save a trained model to disk using joblib.

    Args:
        model: Trained model object.
        filepath: Path where to save the model.
        metadata: Optional dictionary with model metadata (organ name, metrics, etc.).

    Example:
        >>> save_model(model, "models/liver/linear_model.pkl",
        ...           metadata={'organ': 'liver', 'model_type': 'linear'})
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Save model and metadata together
    save_dict = {
        'model': model,
        'metadata': metadata or {}
    }

    joblib.dump(save_dict, filepath)
    print(f"Model saved to {filepath}")


def load_model(filepath: str) -> Any:
    """
    Load a trained model from disk.

    Args:
        filepath: Path to the saved model file.

    Returns:
        Loaded model object.

    Example:
        >>> model = load_model("models/liver/linear_model.pkl")
        >>> predictions = model.predict(X_test)
    """
    filepath = Path(filepath)

    if not filepath.exists():
        raise FileNotFoundError(f"Model file not found: {filepath}")

    loaded = joblib.load(filepath)

    # Handle both old format (just model) and new format (dict with model + metadata)
    if isinstance(loaded, dict) and 'model' in loaded:
        model = loaded['model']
        metadata = loaded.get('metadata', {})
        if metadata:
            print(f"Loaded model with metadata: {metadata}")
    else:
        model = loaded

    print(f"Model loaded from {filepath}")
    return model


def train_organ_models(organ_datasets: Dict,
                      splits: Dict,
                      organ_name: str,
                      save_dir: str = "models",
                      train_linear: bool = True,
                      train_nonlinear: bool = True,
                      nonlinear_type: str = 'hist_gb') -> Dict[str, Any]:
    """
    Train both linear and non-linear models for a specific organ.

    Args:
        organ_datasets: Dictionary containing (X, y) tuples for each organ.
        splits: Dictionary containing split data for the organ.
        organ_name: Name of the organ to train models for.
        save_dir: Directory to save trained models.
        train_linear: Whether to train linear model.
        train_nonlinear: Whether to train non-linear model.
        nonlinear_type: Type of non-linear model to use.

    Returns:
        Dictionary with trained models.

    Example:
        >>> models = train_organ_models(organ_datasets, splits, 'liver')
    """
    X_train = splits['X_train']
    y_train = splits['y_train']

    models = {}
    save_path = Path(save_dir) / organ_name
    save_path.mkdir(parents=True, exist_ok=True)

    if train_linear:
        print(f"\n=== Training Linear Model for {organ_name} ===")
        linear_model = train_linear_model(X_train, y_train, model_type='linear')
        models['linear'] = linear_model

        save_model(
            linear_model,
            save_path / "linear_model.pkl",
            metadata={'organ': organ_name, 'model_type': 'linear'}
        )

    if train_nonlinear:
        print(f"\n=== Training Non-Linear Model ({nonlinear_type}) for {organ_name} ===")
        nonlinear_model = train_nonlinear_model(X_train, y_train, model_type=nonlinear_type)
        models['nonlinear'] = nonlinear_model

        save_model(
            nonlinear_model,
            save_path / f"{nonlinear_type}_model.pkl",
            metadata={'organ': organ_name, 'model_type': nonlinear_type}
        )

    return models
