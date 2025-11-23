"""Test script to verify notebook data loading works"""
import sys
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Setup paths
project_root = Path(__file__).parent
src_path = project_root / 'src'
sys.path.insert(0, str(src_path))

print(f"Project root: {project_root}")
print(f"Source path: {src_path}")

# Import modules
from organ_aging import config, data_loading

# Load configuration
print("\n=== Loading configuration ===")
paths_config = config.load_paths_config(str(project_root / "configs" / "paths.yaml"))
print(f"Raw data directory: {paths_config['raw_data_dir']}")
print(f"Number of NHANES files: {len(paths_config['nhanes_files'])}")

# Load NHANES tables with project_root
print("\n=== Loading NHANES data files ===")
tables = data_loading.load_nhanes_tables(paths_config, project_root=project_root)
print(f"\nSuccessfully loaded {len(tables)} tables")

# Display summary
print("\nTable summaries:")
for table_name, df in tables.items():
    print(f"\n{table_name.upper()}:")
    print(f"  Shape: {df.shape}")
    print(f"  Sample columns: {', '.join(df.columns[:5].tolist())}")

# Merge tables
print("\n=== Merging NHANES tables on SEQN ===")
merged_df = data_loading.merge_nhanes_tables(tables)
print(f"\nFinal merged dataset:")
print(f"  Rows: {merged_df.shape[0]:,}")
print(f"  Columns: {merged_df.shape[1]}")

print("\n=== SUCCESS! Data loading works ===")
