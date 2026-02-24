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
    rows = []
    with open(filepath, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            rows.append(row)

    if not rows:
        return []

    num_cols = max(len(r) for r in rows)
    columns = [[] for _ in range(num_cols)]
    for row in rows:
        for j in range(num_cols):
            value = row[j].strip() if j < len(row) else ""
            columns[j].append(value)

    return columns
