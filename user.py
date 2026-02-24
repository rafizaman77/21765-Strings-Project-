"""
User Module
Input: command line (csv file name, percentage, minimum length).
Output: human-readable presentation of matching substrings per column.
"""

import argparse
import sys

from kernel import run

# grab the command line arguments
def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="""Find substrings of 2+ chars that appear in at least X%% 
                       of entries per CSV column.""",
    )
    parser.add_argument(
        "csv_file",
        help="Path to the CSV file",
    )
    parser.add_argument(
        "-p", "--percentage",
        type=float,
        default=60.0,
        help="""Percentage of entries that must contain 
                the substring (default: 60)""",
    )   
    parser.add_argument(
        "-m", "--min-length",
        type=int,
        default=2,
        help="Minimum number of characters in a match (default: 2)",
    )
    args = parser.parse_args(argv)
    if args.percentage < 0 or args.percentage > 100:
        parser.error("percentage must be between 0 and 100")
    if args.min_length < 1:
        parser.error("min-length must be at least 1")
    return args


def present_results(csv_path: str, results: 
                    list[tuple[int, int, list[tuple[str, int]]]]) -> None:
    """Print results to stdout."""
    print(f"CSV: {csv_path}")
    print()
    for col_idx, total, matches in results:
        print(f"Column {col_idx}:")
        if not matches:
            print("  (no matches)")
        else:
            for sub, count in matches:
                print(f"""  \"{sub}\" appeared {count} 
                      times out of {total} entries""")
        print()


def main(argv=None) -> None:
    args = parse_args(argv)
    threshold = args.percentage / 100.0
    results = run(args.csv_file, threshold, args.min_length)
    present_results(args.csv_file, results)


if __name__ == "__main__":
    main(sys.argv[1:])
