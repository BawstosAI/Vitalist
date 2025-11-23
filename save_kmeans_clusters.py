"""
Script to run K-means clustering and save results to age_gaps.parquet
This replicates the clustering from notebook 05 and saves the results
"""
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Setup paths
project_root = Path(__file__).parent
src_path = project_root / 'src'
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

import pandas as pd
import numpy as np
from organ_aging import clustering

print("=" * 60)
print("K-MEANS CLUSTERING - SAVE RESULTS")
print("=" * 60)

# Load age gaps data
age_gaps_path = project_root / "data" / "processed" / "age_gaps.parquet"
age_gaps_df = pd.read_parquet(age_gaps_path)
print(f"\n> Loaded {len(age_gaps_df)} individuals")

# Get gap columns
gap_columns = [col for col in age_gaps_df.columns if col.endswith('_age_gap') and col != 'max_age_gap']
print(f"> Found {len(gap_columns)} organ gap columns")

# Extract gap data (drop NaN if any)
X_gaps = age_gaps_df[gap_columns].dropna()
print(f"> {len(X_gaps)} individuals for clustering (after removing NaN)")

# Perform K-means clustering with k=3
print("\n> Running K-means clustering (k=3)...")
cluster_labels, kmeans_model = clustering.perform_clustering(
    X_gaps.values,
    method='kmeans',
    n_clusters=3
)

print(f"> K-means clustering complete")
print(f"  Inertia: {kmeans_model.inertia_:.2f}")

# Add cluster labels to full dataset (remap 0,1,2 to 1,2,3)
age_gaps_df['cluster_kmeans'] = -1  # Default for individuals not clustered
age_gaps_df.loc[X_gaps.index, 'cluster_kmeans'] = cluster_labels + 1  # +1 to get clusters 1,2,3

# Save back to parquet
output_path = project_root / "data" / "processed" / "age_gaps.parquet"
age_gaps_df.to_parquet(output_path, index=True)

print(f"\n> Saved clustering results to: {output_path}")
print(f"\n> Cluster distribution:")
cluster_counts = age_gaps_df[age_gaps_df['cluster_kmeans'] >= 0]['cluster_kmeans'].value_counts().sort_index()
for cluster_id, count in cluster_counts.items():
    pct = 100 * count / len(age_gaps_df)
    print(f"    Cluster {cluster_id}: {count} individuals ({pct:.1f}%)")

print("\n" + "=" * 60)
print("SUCCESS: CLUSTERING RESULTS SAVED")
print("=" * 60)
print("\nThe 'cluster_kmeans' column is now available for:")
print("  - Web app data export (notebook 07)")
print("  - Further analysis and visualization")
print("  - Jury presentation")
