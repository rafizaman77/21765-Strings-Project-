"""
Find Matching Substrings Module
Input:  a column (list of strings), threshold fraction (0..1), minimum substring 
        length. Iterates over substring lengths until no more matches are found.
Output: list of (substring, count) for substrings that appear 
        in >= threshold fraction of entries.
"""

from collections import defaultdict


def find_matching_substrings(
    column: list[str],
    threshold: float,
    min_len: int,
) -> list[tuple[str, int]]:
    """
    Find all substrings that have length >= min_len that 
    appear in at least threshold fraction of the column entries.
    
    Args:
        column: List of strings (cell values from one CSV column)
        threshold: Fraction (0.0 to 1.0) of entries that must contain substring
        min_len: Minimum substring length to search for
    
    Returns:
        List of (substring, count) tuples, sorted by length (longest first), 
        then alphabetically. Each substring appears in at least threshold 
        fraction of entries.
    """
    n = len(column)
    if n == 0:
        return []
    min_count = max(1, int(threshold * n))

    # Collect all unique substrings by length: length -> {substring}
    # For each length L, count how many entries contain each substring of length L
    results = []

    # Find the maximum cell length to determine search range
    cell_lengths = [len(cell) for cell in column]
    max_cell_length = max(cell_lengths) if cell_lengths else 0
    
    # Process each substring length from minimum to maximum
    for substring_length in range(min_len, max_cell_length + 1):
        # Track how many entries contain each substring
        entry_containment = defaultdict(int)
        
        for cell_value in column:
            # Track unique substrings per cell to avoid double counting
            cell_substrings = set()
            cell_length = len(cell_value)
            
            # Extract all substrings of current length from this cell
            for start_pos in range(cell_length - substring_length + 1):
                extracted_substring = cell_value[start_pos : start_pos + substring_length]
                if extracted_substring not in cell_substrings:
                    cell_substrings.add(extracted_substring)
                    entry_containment[extracted_substring] += 1

        # Collect substrings that meet the threshold
        for substring, entry_count in entry_containment.items():
            if entry_count >= min_count:
                results.append((substring, entry_count))

    # Deduplicate by substring (same substring can qualify at multiple lengths)
    # Use a dictionary to track unique substrings and their counts
    unique_matches = {}
    for substring, occurrence_count in results:
        if substring not in unique_matches or occurrence_count > unique_matches[substring]:
            unique_matches[substring] = occurrence_count
    
    # Convert to list and sort: longest first, then alphabetically
    final_results = [(sub, unique_matches[sub]) for sub in unique_matches]
    final_results.sort(key=lambda x: (-len(x[0]), x[0]))

    return final_results
