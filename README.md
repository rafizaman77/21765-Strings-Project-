# 21-765 Parallel Computation and Scientific Computing — Take-home Midterm (Spring 2026)

## Common Substrings CSV Analyzer

This project solves the following problem: find **groups of 2 or more consecutive characters** (including spaces or symbols) that appear in **at least a given percentage** of the entries in each column of a CSV file. Substrings are reported per column with their occurrence counts.

## Project Structure

The project is organized into the following modules:

- **`main.py`**: Entry point that runs the user module
- **`user.py`**: Handles command-line arguments and presents results
- **`kernel.py`**: Orchestrates data extraction and substring matching
- **`data_extraction.py`**: Reads CSV files and extracts columns
- **`find_matches.py`**: Finds matching substrings in columns

## How to Run

### Basic Usage

Run with default settings (60% threshold, minimum length 2):

```bash
python3 main.py w5-Sample.csv
```

### Custom Parameters

Specify custom threshold percentage and minimum substring length:

```bash
python3 main.py <csv_file> -p <percentage> -m <min_length>
```

### Examples

```bash
# Default (60% threshold, min length 2)
python3 main.py w5-Sample.csv

# Custom threshold (15%) and min length (4)
python3 main.py w5-Sample.csv -p 15 -m 4

# Custom threshold (80%) with default min length (2)
python3 main.py w5-Sample.csv -p 80
```

## Requirements

- **Python**: 3.10 or higher
- **Packages**: No external packages required; uses only Python standard library:
  - `argparse` (command-line argument parsing)
  - `csv` (CSV file reading)
  - `collections` (defaultdict for counting)

## Module APIs

### User Module (`user.py`)
- **Input**: Command-line arguments (CSV file path, percentage, minimum length)
- **Output**: Human-readable presentation of results
- **Functions**:
  - `parse_args(argv)`: Parses command-line arguments
  - `present_results(csv_path, results)`: Formats and displays results
  - `main(argv)`: Main entry point

### Kernel Module (`kernel.py`)
- **Input**: CSV file path, threshold fraction (0.0-1.0), minimum substring length
- **Output**: List of tuples `(column_index, total_entries, list of (substring, count))`
- **Functions**:
  - `run(csv_path, threshold, min_len)`: Orchestrates the analysis

### Data Extraction Module (`data_extraction.py`)
- **Input**: Path to CSV file
- **Output**: List of columns, where each column is a list of cell values (strings)
- **Functions**:
  - `read_columns(filepath)`: Reads CSV and returns columns

### Find Matches Module (`find_matches.py`)
- **Input**: Column (list of strings), threshold fraction, minimum substring length
- **Output**: List of `(substring, count)` tuples for substrings appearing in ≥threshold fraction of entries
- **Functions**:
  - `find_matching_substrings(column, threshold, min_len)`: Finds all qualifying substrings

## Algorithm Description

The algorithm finds common substrings by:

1. **Extracting columns** from the CSV file
2. **For each column**:
   - Calculate the minimum count required (threshold × number of entries)
   - For each substring length from `min_len` to the maximum cell length:
     - Extract all substrings of that length from all cells
     - Count how many distinct entries contain each substring
     - Collect substrings that appear in at least the threshold percentage
   - Deduplicate results (same substring may qualify at multiple lengths)
   - Sort by length (longest first), then alphabetically

**Time Complexity**: For a column with N entries and average length L:
- O(N × L²) - for each length, we scan each cell and extract substrings
- The algorithm iterates through all possible substring lengths, making it O(N × L³) in the worst case

## Author

Rafi Zaman

## Team

- Gabe Pacella
