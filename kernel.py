"""
Kernel Module
Input: options (csv path, threshold fraction, min substring length).
Detects data file format, calls data extraction and find_matching_substrings.
Output: structured results ready for display (list of per-column match lists).
"""

from data_extraction import read_columns
from find_matches import find_matching_substrings

def run(csv_path: str, threshold: float, 
        min_len: int) -> list[tuple[int, int, list[tuple[str, int]]]]:
    """
    Read the CSV file, find matching substrings for each column, 
    and return the results.
    
    Args:
        csv_path: Path to the CSV file
        threshold: Fraction (0.0 to 1.0) of entries that must contain substring
        min_len: Minimum substring length to search for
    
    Returns:
        List of tuples: (column_index, total_entries, list of (substring, count))
    """
    columns = read_columns(csv_path)
    if not columns:
        return []

    # Process each column and collect results
    results = []
    for column_index in range(len(columns)):
        column_data = columns[column_index]
        column_matches = find_matching_substrings(column_data, threshold, min_len)
        entry_count = len(column_data)
        results.append((column_index, entry_count, column_matches))

    return results
