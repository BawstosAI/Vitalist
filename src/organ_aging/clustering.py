"""
Clustering and dimensionality reduction for organ aging analysis.

This module provides exploratory analysis tools using PCA, UMAP, and clustering
to identify patterns in organ aging profiles.
"""

import pandas as pd
import numpy as np
from typing import Tuple, Optional, Any
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import warnings


def apply_pca(X: pd.DataFrame,
             n_components: int = 2,
             scale: bool = True) -> Tuple[np.ndarray, Any]:
    """
    Apply PCA for dimensionality reduction.

    Args:
        X: Feature matrix (e.g., age gap vectors).
        n_components: Number of principal components to retain.
        scale: Whether to scale features before PCA.

    Returns:
        Tuple of (transformed data, fitted PCA model).

    Example:
        >>> X_pca, pca_model = apply_pca(age_gaps_df, n_components=2)
        >>> print(f"Explained variance: {pca_model.explained_variance_ratio_}")
    """
    if scale:
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
    else:
        X_scaled = X.values if isinstance(X, pd.DataFrame) else X

    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    print(f"\nPCA Results:")
    print(f"  Components: {n_components}")
    print(f"  Explained variance ratio: {pca.explained_variance_ratio_}")
    print(f"  Cumulative explained variance: {pca.explained_variance_ratio_.sum():.3f}")

    return X_pca, pca


def apply_umap(X: pd.DataFrame,
              n_components: int = 2,
              n_neighbors: int = 15,
              min_dist: float = 0.1,
              metric: str = 'euclidean') -> Tuple[np.ndarray, Any]:
    """
    Apply UMAP for dimensionality reduction.

    Requires the 'umap-learn' package to be installed.

    Args:
        X: Feature matrix (e.g., age gap vectors).
        n_components: Number of dimensions to reduce to.
        n_neighbors: Number of neighbors for UMAP.
        min_dist: Minimum distance between points in embedding.
        metric: Distance metric to use.

    Returns:
        Tuple of (transformed data, fitted UMAP model).

    Example:
        >>> # Requires: pip install umap-learn
        >>> X_umap, umap_model = apply_umap(age_gaps_df, n_components=2)

    Note:
        If UMAP is not installed, this function will raise an ImportError
        with installation instructions.
    """
    try:
        import umap
    except ImportError:
        raise ImportError(
            "UMAP package not installed. Install with: pip install umap-learn\n"
            "For faster performance with CUDA support: pip install cuml (requires GPU)"
        )

    X_values = X.values if isinstance(X, pd.DataFrame) else X

    umap_model = umap.UMAP(
        n_components=n_components,
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        metric=metric,
        random_state=42
    )

    print(f"\nUMAP transformation...")
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        X_umap = umap_model.fit_transform(X_values)

    print(f"  Shape: {X_umap.shape}")

    return X_umap, umap_model


def perform_clustering(X: np.ndarray,
                      method: str = 'kmeans',
                      n_clusters: int = 3,
                      **kwargs) -> Tuple[np.ndarray, Any]:
    """
    Perform clustering on data.

    Args:
        X: Feature matrix or embedding.
        method: Clustering method ('kmeans', 'hdbscan').
        n_clusters: Number of clusters (for kmeans).
        **kwargs: Additional parameters for clustering algorithm.

    Returns:
        Tuple of (cluster labels, fitted clustering model).

    Example:
        >>> labels, model = perform_clustering(X_umap, method='kmeans', n_clusters=4)
        >>> print(f"Cluster distribution: {np.bincount(labels)}")
    """
    if method == 'kmeans':
        default_params = {
            'n_clusters': n_clusters,
            'random_state': 42,
            'n_init': 10
        }
        default_params.update(kwargs)

        model = KMeans(**default_params)
        labels = model.fit_predict(X)

        print(f"\nKMeans Clustering:")
        print(f"  Clusters: {n_clusters}")
        print(f"  Inertia: {model.inertia_:.2f}")

    elif method == 'hdbscan':
        try:
            import hdbscan
        except ImportError:
            raise ImportError("HDBSCAN not installed. Install with: pip install hdbscan")

        default_params = {
            'min_cluster_size': 10,
            'min_samples': 5
        }
        default_params.update(kwargs)

        model = hdbscan.HDBSCAN(**default_params)
        labels = model.fit_predict(X)

        n_clusters_found = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise = np.sum(labels == -1)

        print(f"\nHDBSCAN Clustering:")
        print(f"  Clusters found: {n_clusters_found}")
        print(f"  Noise points: {n_noise} ({100*n_noise/len(labels):.1f}%)")

    else:
        raise ValueError(f"Unknown clustering method: {method}. Use 'kmeans' or 'hdbscan'.")

    # Print cluster distribution
    unique_labels, counts = np.unique(labels, return_counts=True)
    print(f"\n  Cluster distribution:")
    for label, count in zip(unique_labels, counts):
        cluster_name = "Noise" if label == -1 else f"Cluster {label}"
        print(f"    {cluster_name}: {count} ({100*count/len(labels):.1f}%)")

    return labels, model


def create_embedding_dataframe(X_embedded: np.ndarray,
                               df: pd.DataFrame,
                               labels: Optional[np.ndarray] = None,
                               method: str = 'umap') -> pd.DataFrame:
    """
    Create a DataFrame with embedding coordinates and metadata.

    Args:
        X_embedded: Embedding coordinates (n_samples, n_components).
        df: Original DataFrame with metadata.
        labels: Optional cluster labels.
        method: Name of the embedding method (for column naming).

    Returns:
        DataFrame with embedding coordinates, metadata, and optional cluster labels.

    Example:
        >>> embed_df = create_embedding_dataframe(X_umap, df, labels=cluster_labels, method='umap')
        >>> print(embed_df.columns)
    """
    n_components = X_embedded.shape[1]

    # Create base DataFrame with embedding coordinates
    embed_df = pd.DataFrame(
        X_embedded,
        columns=[f'{method}_{i+1}' for i in range(n_components)],
        index=df.index
    )

    # Add metadata from original DataFrame
    for col in df.columns:
        if col not in embed_df.columns:
            embed_df[col] = df[col]

    # Add cluster labels if provided
    if labels is not None:
        embed_df['cluster'] = labels

    return embed_df


def analyze_cluster_characteristics(df: pd.DataFrame,
                                   cluster_col: str = 'cluster',
                                   gap_columns: Optional[list] = None) -> pd.DataFrame:
    """
    Analyze characteristics of each cluster.

    Args:
        df: DataFrame with cluster labels and age gap columns.
        cluster_col: Name of the cluster label column.
        gap_columns: List of gap column names. If None, auto-detects.

    Returns:
        DataFrame with cluster characteristics.

    Example:
        >>> characteristics = analyze_cluster_characteristics(embed_df)
        >>> print(characteristics)
    """
    if gap_columns is None:
        gap_columns = [col for col in df.columns if col.endswith('_age_gap')]

    if cluster_col not in df.columns:
        raise ValueError(f"Cluster column '{cluster_col}' not found in DataFrame")

    # Calculate mean gaps for each cluster
    cluster_chars = df.groupby(cluster_col)[gap_columns].mean()

    # Add cluster sizes
    cluster_chars['n_samples'] = df.groupby(cluster_col).size()

    # Add mean chronological age if available
    if 'AGE' in df.columns:
        cluster_chars['mean_age'] = df.groupby(cluster_col)['AGE'].mean()

    print("\nCluster Characteristics:")
    print(cluster_chars)

    return cluster_chars


def visualize_embedding(embed_df: pd.DataFrame,
                       x_col: str = 'umap_1',
                       y_col: str = 'umap_2',
                       color_by: Optional[str] = None,
                       figsize: Tuple[int, int] = (10, 8)) -> Any:
    """
    Visualize 2D embedding with optional coloring.

    Args:
        embed_df: DataFrame with embedding coordinates.
        x_col: Column name for x-axis.
        y_col: Column name for y-axis.
        color_by: Optional column name to color points by.
        figsize: Figure size.

    Returns:
        Matplotlib figure object.

    Example:
        >>> fig = visualize_embedding(embed_df, color_by='cluster')
        >>> plt.show()
    """
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=figsize)

    if color_by and color_by in embed_df.columns:
        # Colored by specified column
        if embed_df[color_by].dtype in [np.float64, np.int64]:
            scatter = ax.scatter(embed_df[x_col], embed_df[y_col],
                               c=embed_df[color_by], cmap='viridis',
                               alpha=0.6, s=20)
            plt.colorbar(scatter, ax=ax, label=color_by)
        else:
            # Categorical coloring
            categories = embed_df[color_by].unique()
            for category in categories:
                mask = embed_df[color_by] == category
                ax.scatter(embed_df.loc[mask, x_col],
                          embed_df.loc[mask, y_col],
                          label=f'{color_by}={category}',
                          alpha=0.6, s=20)
            ax.legend()
    else:
        # No coloring
        ax.scatter(embed_df[x_col], embed_df[y_col], alpha=0.6, s=20)

    ax.set_xlabel(x_col.upper().replace('_', ' '))
    ax.set_ylabel(y_col.upper().replace('_', ' '))
    ax.set_title(f'{x_col.split("_")[0].upper()} Embedding of Organ Age Gaps',
                fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig
