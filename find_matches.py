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

    max_len = max(len(cell) for cell in column)
    for length in range(min_len, max_len + 1):
        # substring -> number of entries that contain it
        containment_count = defaultdict(int)
        for cell in column:
            seen_this_cell = set()
            for start in range(len(cell) - length + 1):
                sub = cell[start : start + length]
                if sub not in seen_this_cell:
                    seen_this_cell.add(sub)
                    containment_count[sub] += 1

        for sub, count in containment_count.items():
            if count >= min_count:
                results.append((sub, count))

    # Deduplicate by substring (same substring can qualify at multiple lengths)
    seen = {}
    for sub, count in results:
        if sub not in seen:
            seen[sub] = count
    results = [(sub, seen[sub]) for sub in sorted(seen.keys(), key=lambda s: (-len(s), s))]

    return results
