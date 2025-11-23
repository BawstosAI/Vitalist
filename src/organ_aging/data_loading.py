"""
NHANES data loading utilities.

This module provides functions for loading and merging NHANES data files (XPT or CSV format).
"""

import pandas as pd
from pathlib import Path
from typing import Dict, List
import warnings


def load_nhanes_tables(paths_config: Dict, project_root: Path = None) -> Dict[str, pd.DataFrame]:
    """
    Load NHANES data tables from files specified in configuration.

    Supports both XPT (SAS Transport) and CSV file formats.

    Args:
        paths_config: Dictionary containing:
            - 'raw_data_dir': Base directory for raw data files
            - 'nhanes_files': Dict mapping table names to filenames
        project_root: Optional project root path for resolving relative paths.
                     If not provided, paths are treated as relative to current working directory.

    Returns:
        Dictionary mapping table names to pandas DataFrames.

    Raises:
        FileNotFoundError: If a specified data file cannot be found.
        ValueError: If file format is not supported.

    Example:
        >>> paths = {
        ...     'raw_data_dir': 'data/raw',
        ...     'nhanes_files': {'demographics': 'DEMO.XPT'}
        ... }
        >>> tables = load_nhanes_tables(paths, project_root=Path('/path/to/project'))
        >>> print(tables['demographics'].shape)
    """
    raw_data_dir = Path(paths_config['raw_data_dir'])

    # Convert to absolute path using project_root if provided
    if project_root is not None and not raw_data_dir.is_absolute():
        raw_data_dir = project_root / raw_data_dir

    nhanes_files = paths_config['nhanes_files']

    tables = {}

    for table_name, filename in nhanes_files.items():
        file_path = raw_data_dir / filename

        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")

        # Determine file format and load accordingly
        if file_path.suffix.upper() == '.XPT':
            try:
                df = pd.read_sas(str(file_path), format='xport')
            except Exception as e:
                raise ValueError(f"Error reading XPT file {file_path}: {e}")

        elif file_path.suffix.upper() == '.CSV':
            try:
                df = pd.read_csv(file_path)
            except Exception as e:
                raise ValueError(f"Error reading CSV file {file_path}: {e}")

        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

        # Convert column names to uppercase for consistency
        df.columns = df.columns.str.upper()

        tables[table_name] = df
        print(f"Loaded {table_name}: {df.shape[0]} rows, {df.shape[1]} columns")

    return tables


def merge_nhanes_tables(tables_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Merge multiple NHANES tables on the SEQN (sequence number) column.

    Performs inner joins to keep only records present in all tables.

    Args:
        tables_dict: Dictionary mapping table names to DataFrames.
                    All DataFrames must contain a 'SEQN' column.

    Returns:
        Merged DataFrame containing all columns from all input tables.

    Raises:
        ValueError: If SEQN column is missing from any table.

    Example:
        >>> tables = {
        ...     'demo': pd.DataFrame({'SEQN': [1, 2], 'AGE': [25, 35]}),
        ...     'bio': pd.DataFrame({'SEQN': [1, 2], 'ALT': [20, 25]})
        ... }
        >>> merged = merge_nhanes_tables(tables)
        >>> print(merged.columns.tolist())
        ['SEQN', 'AGE', 'ALT']
    """
    if not tables_dict:
        raise ValueError("No tables provided for merging")

    # Verify all tables have SEQN column
    for table_name, df in tables_dict.items():
        if 'SEQN' not in df.columns:
            raise ValueError(f"Table '{table_name}' does not contain SEQN column")

    # Start with the first table
    table_names = list(tables_dict.keys())
    merged_df = tables_dict[table_names[0]].copy()
    print(f"Starting merge with {table_names[0]}: {merged_df.shape}")

    # Merge remaining tables
    for table_name in table_names[1:]:
        df = tables_dict[table_name]

        # Get overlapping columns (excluding SEQN)
        overlap_cols = set(merged_df.columns) & set(df.columns) - {'SEQN'}

        if overlap_cols:
            warnings.warn(
                f"Overlapping columns found between existing merged table and '{table_name}': "
                f"{overlap_cols}. Suffixes will be added."
            )

        merged_df = merged_df.merge(
            df,
            on='SEQN',
            how='inner',
            suffixes=('', f'_{table_name}')
        )

        print(f"After merging {table_name}: {merged_df.shape}")

    print(f"\nFinal merged dataset: {merged_df.shape[0]} rows, {merged_df.shape[1]} columns")

    return merged_df


def load_and_merge_nhanes(paths_config: Dict, project_root: Path = None) -> pd.DataFrame:
    """
    Convenience function to load and merge NHANES tables in one step.

    Args:
        paths_config: Paths configuration dictionary.
        project_root: Optional project root path for resolving relative paths.

    Returns:
        Merged DataFrame containing all NHANES data.

    Example:
        >>> config = {'raw_data_dir': 'data/raw', 'nhanes_files': {...}}
        >>> df = load_and_merge_nhanes(config, project_root=Path('/path/to/project'))
    """
    tables = load_nhanes_tables(paths_config, project_root=project_root)
    merged = merge_nhanes_tables(tables)
    return merged
