"""
Main entry point for the Common Substrings CSV analyzer.
Runs the user module.
"""
import sys

if __name__ == "__main__":
    from user import main
    main(sys.argv[1:])
