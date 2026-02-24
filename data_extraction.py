"""
Data Extraction Module
Input: path to a CSV data file.
Output: list of columns; each column is a list of cell values (strings).
"""

import csv


def read_columns(filepath: str) -> list[list[str]]:
    """
    Read the CSV file and return list of columns.
    
    Args:
        filepath: Path to the CSV file
    
    Returns:
        List of columns, where each column is a list of cell values (strings)
    """
    # First pass: determine maximum number of columns
    max_cols = 0
    row_count = 0
    with open(filepath, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # Skip empty rows
                max_cols = max(max_cols, len(row))
                row_count += 1
    
    if max_cols == 0 or row_count == 0:
        return []
    
    # Second pass: build columns directly
    columns = [[] for _ in range(max_cols)]
    with open(filepath, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            # Add each cell to its corresponding column
            for col_idx in range(max_cols):
                if col_idx < len(row):
                    columns[col_idx].append(row[col_idx].strip())
                else:
                    columns[col_idx].append("")
    
    return columns
