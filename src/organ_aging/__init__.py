"""
Organ Aging Analysis Package

This package provides tools for analyzing organ-specific aging patterns using NHANES data.
It implements "organ clocks" - machine learning models that predict chronological age from
organ-specific biomarkers, enabling the calculation of biological age gaps for different organs.
"""

__version__ = "0.1.0"
__author__ = "Vitalist Team"

from . import config
from . import data_loading
from . import preprocessing
from . import features
from . import models
from . import evaluation
from . import explainability
from . import analysis
from . import visualization
from . import clustering

__all__ = [
    "config",
    "data_loading",
    "preprocessing",
    "features",
    "models",
    "evaluation",
    "explainability",
    "analysis",
    "visualization",
    "clustering",
]
