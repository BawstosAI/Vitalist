"""Tests for clustering module."""
import pytest
import pandas as pd
import numpy as np
from src.organ_aging.clustering import (
    apply_pca,
    apply_umap,
    perform_clustering
)


class TestClustering:
    """Test clustering and dimensionality reduction functions."""

    def test_apply_pca_reduces_dimensions(self):
        """Test PCA dimensionality reduction."""
        X = pd.DataFrame(np.random.randn(50, 10))

        X_pca, pca_model = apply_pca(X, n_components=2)
        assert X_pca.shape == (50, 2)
        assert pca_model is not None
        assert hasattr(pca_model, 'explained_variance_ratio_')

    def test_apply_umap_reduces_dimensions(self):
        """Test UMAP dimensionality reduction."""
        X = pd.DataFrame(np.random.randn(50, 10))

        X_umap, umap_model = apply_umap(X, n_components=2)
        assert X_umap.shape == (50, 2)
        assert umap_model is not None

    def test_perform_clustering_assigns_labels(self):
        """Test clustering algorithm."""
        X = pd.DataFrame(np.random.randn(50, 2))

        labels, model = perform_clustering(X, method='kmeans', n_clusters=3)
        assert len(labels) == 50
        assert len(np.unique(labels)) <= 3
        assert model is not None
