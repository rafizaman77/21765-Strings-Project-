# Take Home Mid-Term Spring 2026

**Due on 11:59pm Feb 23, 2026, by e-mail to florin@cmu.edu**

---

**Your Name:** Rafi Zaman

**Coding Team colleagues** (team of up to 4 members sharing work on the same code) in the order of your collaboration with them (the most collaboration on top):

1. Gabe Pacella
2. 
3. 
4. 

---

## Rules:
- Submit one document per student
- Submit one code archive per team
- Use any help available, including me, people in the team, other people you know, LLMs, online documentation, etc.

---

## Problem to solve (ambiguous, management style formulation):

Find groups of 2 or more consecutive characters (as many as possible, including spaces or symbols) which can be found in at least 60% of the entries in a column of a csv file.

---

## Deliverables:

1. This document filled individually by every student; some of the answers may be shared.
2. Archive of the code; each module in a separate file.

---

## Suggested structure of the solution (modules):

Modify if your structure is different.

**User:** yes, it is useful to consider the user as a module for documentation purposes
- Input: command line options, e.g. csv file name, percentage of string matches (default 60%), minimum number of characters in the match (default 2)
- Output: presentation and meaning of the results

**Kernel:** 
- Input: extract information from the command line options
- detect data file format
- call the other modules as needed 
- Output: format and display results

**Data extraction:** 
- Input: read the data file 
- Output: return the columns as separate entities

**Find matching substrings for the entries in a column:**
- Input: receive a column
- iterate the search process until no more matches are found
- Output: return the results

---

## Assumptions:

State unambiguously any assumptions you made to solve the problem (ask me for clarifications if the original formulation doesn't say much to you).
Motivate your assumptions if needed.

**Your assumptions here:**

1. **CSV Format and Parsing**: I assumed the CSV file follows standard comma-separated format as handled by Python's `csv.reader`. Looking at the implementation in `data_extraction.py`, I can see that empty rows are explicitly skipped (line 26 checks `if row:` and line 38 checks `if not row: continue`). The code uses UTF-8 encoding with error replacement (`encoding="utf-8", errors="replace"`), which means it can handle any characters including spaces, symbols, and special characters. I also noticed that cells are trimmed using `.strip()` on line 43, which removes leading and trailing whitespace. This assumption was necessary because the problem statement didn't specify how to handle whitespace or special characters.

2. **Substring Matching Semantics**: I interpreted "appears in" to mean substring containment anywhere within the cell text, not as whole words. This is evident in `find_matches.py` where the algorithm uses a sliding window approach (lines 55-59) that extracts all possible substrings of a given length from each cell. Importantly, I implemented deduplication per cell using a `set()` called `cell_substrings` (line 51), which ensures that if the same substring appears multiple times within a single cell, it's only counted once for that entry. This prevents cells with repeated patterns from skewing the results unfairly.

3. **Threshold Calculation and Edge Cases**: The threshold percentage is applied independently to each column, which makes sense since different columns may have different data characteristics. In `find_matches.py` line 34, I calculate `min_count = max(1, int(threshold * n))`, which ensures that even with very small columns or low thresholds, at least one entry must contain the substring. The `max(1, ...)` prevents the edge case where rounding down could result in zero required matches. This approach guarantees that any reported substring actually appears in at least one entry, maintaining the semantic meaning of "at least X%".

4. **Output Formatting and Deduplication**: I assumed that results should be comprehensive - reporting all qualifying substrings even if they overlap or are substrings of longer matches. The deduplication logic in lines 68-71 of `find_matches.py` handles cases where the same substring qualifies at multiple lengths (e.g., "di" might qualify at length 2, 3, and 4). When this happens, I keep the maximum count encountered. The final sorting (line 75) uses `key=lambda x: (-len(x[0]), x[0])`, which sorts by negative length (longest first) then alphabetically, making longer, more specific patterns appear first in the output. 

---

## Code documentation:

### 1. Draw the diagram of the modules. List APIs describing precisely the communication channels (input and output) between modules.

**Module Diagram:**

```
[Command Line] 
    |
    v
[User Module]
    | (csv_path, percentage, min_length)
    v
[Kernel Module]
    | (csv_path)
    v
[Data Extraction Module]
    | (columns: list[list[str]])
    v
[Kernel Module]
    | (column, threshold, min_len)
    v
[Find Matches Module]
    | (results: list[tuple[str, int]])
    v
[Kernel Module]
    | (formatted_results)
    v
[User Module]
    | (display)
    v
[Output]
```

**API Documentation:**

**User Module → Kernel Module:**
- **Function**: `run(csv_path: str, threshold: float, min_len: int)` (defined in `kernel.py` line 11)
- **Input**: 
  - `csv_path: str` - Path to the CSV file (extracted from command line args in `user.py` line 19)
  - `threshold: float` - Fraction between 0.0 and 1.0 (converted from percentage in `user.py` line 64: `threshold = args.percentage / 100.0`)
  - `min_len: int` - Minimum substring length (from `user.py` line 32, default 2)
- **Output**: `list[tuple[int, int, list[tuple[str, int]]]]` - List of tuples where each tuple contains:
  - `column_index: int` - Zero-indexed column number
  - `total_entries: int` - Total number of entries in that column
  - `matches: list[tuple[str, int]]` - List of (substring, count) pairs for qualifying substrings
- **Usage**: Called from `user.py` line 65: `results = run(args.csv_file, threshold, args.min_length)`

**Kernel Module → Data Extraction Module:**
- **Function**: `read_columns(filepath: str)` (defined in `data_extraction.py` line 10)
- **Input**: 
  - `filepath: str` - Path to CSV file (passed from `kernel.py` line 25: `columns = read_columns(csv_path)`)
- **Output**: `list[list[str]]` - List of columns, where each column is a list of cell values (strings)
  - Empty file returns empty list (line 31: `return []`)
  - Each inner list represents one column with all its cell values
  - Cells are trimmed of whitespace (line 43: `row[col_idx].strip()`)
  - Missing cells are filled with empty strings (line 45: `columns[col_idx].append("")`)
- **Implementation Note**: Uses two-pass approach - first pass determines max columns (lines 20-28), second pass builds columns directly (lines 33-45)

**Kernel Module → Find Matches Module:**
- **Function**: `find_matching_substrings(column: list[str], threshold: float, min_len: int)` (defined in `find_matches.py` line 12)
- **Input**: 
  - `column: list[str]` - List of cell values from one CSV column (passed from `kernel.py` line 33)
  - `threshold: float` - Fraction of entries that must contain substring (from `kernel.py` line 33)
  - `min_len: int` - Minimum substring length to search for (from `kernel.py` line 33)
- **Output**: `list[tuple[str, int]]` - List of (substring, count) tuples where:
  - `substring: str` - The matching substring
  - `count: int` - Number of distinct entries containing this substring
  - Results are sorted by length (longest first), then alphabetically (line 75)
  - Empty column returns empty list (line 33: `return []`)
- **Usage**: Called from `kernel.py` line 33: `column_matches = find_matching_substrings(column_data, threshold, min_len)`

---

### 2. Which modules should be optimized to increase the sequential execution speed? Present your thoughts about this subject, no implementation needed.

**Your analysis here:**

1. **Find Matches Module (`find_matches.py`)** - This is clearly the computational bottleneck:
   
   Looking at the implementation, the algorithm has three nested loops (lines 45, 49, 55) that create O(N × L³) complexity. The outer loop iterates through all substring lengths from `min_len` to `max_cell_length` (line 45), which can be up to the length of the longest cell. For each length, it processes every cell in the column (line 49), and for each cell, it extracts all possible substrings of that length using a sliding window (line 55). 
   
   The main optimization opportunities I see:
   - **Early termination**: Currently, the code processes all lengths even if no matches are found. We could add a check after processing each length - if `entry_containment` is empty or no substrings meet the threshold, we could potentially skip remaining lengths, though this might not always help since shorter substrings might still qualify.
   - **Data structure efficiency**: The current use of `defaultdict(int)` for counting (line 47) is already quite efficient. However, we could potentially use a more memory-efficient approach if dealing with very large datasets.
   - **Redundant substring extraction**: The current implementation extracts substrings fresh for each length. If we processed from longest to shortest, we could potentially reuse information about longer substrings, but this would require a more complex algorithm redesign.
   - **Parallelization potential**: This module is highly parallelizable (see parallel implementation section), which would be more effective than sequential optimization for multi-core systems.

2. **Data Extraction Module (`data_extraction.py`)** - Minor optimization potential:
   
   The current implementation uses a two-pass approach (lines 20-28 for first pass, 33-45 for second pass). This means the file is read twice, which could be optimized for very large files. However, for typical CSV sizes, this approach is actually quite reasonable because:
   - It allows us to determine the maximum column count upfront, avoiding dynamic resizing
   - The file I/O overhead is usually negligible compared to the substring matching computation
   - The code is simpler and more maintainable
   
   Potential optimizations:
   - **Single-pass approach**: We could read the file once and dynamically resize columns, but this would require more complex logic and potentially more memory allocations
   - **Streaming for very large files**: For files that don't fit in memory, we could process columns incrementally, but this would require significant refactoring
   - **Memory mapping**: For very large CSV files, memory-mapped file access could reduce I/O overhead, but this is likely overkill for most use cases

3. **Kernel Module (`kernel.py`)** - Minimal optimization needed:
   
   This module is essentially an orchestrator with O(C) complexity where C is the number of columns. The loop on line 31 simply iterates through columns and calls the other modules. The overhead here is negligible compared to the substring matching work. The only potential micro-optimization would be using list comprehension instead of explicit loop (e.g., `results = [(i, len(col), find_matching_substrings(col, threshold, min_len)) for i, col in enumerate(columns)]`), but this would have minimal impact and might reduce readability.

4. **User Module (`user.py`)** - No optimization needed:
   
   This module handles I/O and formatting. The argument parsing (lines 13-40) is a one-time cost, and the result presentation (lines 43-59) is O(M) where M is the total number of matches across all columns, which is typically much smaller than the computation time.

**Conclusion**: The Find Matches Module should be the primary focus for optimization, as it dominates the execution time. The other modules are already quite efficient for their roles.

---

### 3. Briefly describe the algorithm for finding matches.
If a data column has N lines, how do you expect the execution time to depend on N?

**Algorithm Description:**

The algorithm implemented in `find_matches.py` works as follows:

1. **Initialization and Validation** (lines 31-34): First, it checks if the column is empty and returns early if so. Then it calculates the minimum count required: `min_count = max(1, int(threshold * n))`. The `max(1, ...)` ensures that even with very small columns or low thresholds, at least one entry must contain the substring.

2. **Determine Search Range** (lines 40-42): The algorithm finds the maximum cell length by creating a list of all cell lengths and taking the maximum. This determines the upper bound for substring length iteration: `max_cell_length = max(cell_lengths) if cell_lengths else 0`.

3. **Iterate Through Substring Lengths** (line 45): For each possible substring length from `min_len` to `max_cell_length`, the algorithm performs substring extraction and counting.

4. **Count Substring Occurrences** (lines 46-59): For each substring length:
   - Initialize `entry_containment` as a `defaultdict(int)` to track how many distinct entries contain each substring
   - For each cell in the column:
     - Create a `set()` called `cell_substrings` to track unique substrings within this cell (this prevents double-counting if the same substring appears multiple times in one cell)
     - Use a sliding window approach: iterate through all possible starting positions (`start_pos` from 0 to `cell_length - substring_length + 1`)
     - Extract the substring using slicing: `cell_value[start_pos : start_pos + substring_length]`
     - If this substring hasn't been seen in this cell before, add it to the set and increment the entry count
   - After processing all cells, collect substrings that appear in at least `min_count` entries (lines 62-64)

5. **Deduplication** (lines 66-71): Since the same substring can qualify at multiple lengths (e.g., "di" might appear in 70% of entries at length 2, and also qualify at length 3 as part of "dis"), we deduplicate the results. The code uses a dictionary `unique_matches` that keeps the maximum count encountered for each substring.

6. **Sorting** (lines 73-75): Finally, convert the dictionary to a list of tuples and sort using `key=lambda x: (-len(x[0]), x[0])`, which sorts by negative length (longest first) then alphabetically. This ensures longer, more specific patterns appear before shorter ones.

**Time Complexity Analysis:**

For a column with N entries and average cell length L:
- **Time complexity**: O(N × L³)
  - Outer loop (line 45): O(L) iterations - we iterate through all possible substring lengths from `min_len` to `max_cell_length`, which is at most L
  - Middle loop (line 49): O(N) iterations - we process each of the N cells in the column
  - Inner loop (line 55): O(L) iterations - for each cell, we slide a window through all possible positions, which is approximately L positions
  - Substring extraction (line 56): O(L) per substring - Python string slicing takes O(L) time
  - Set operations: O(1) average case for set membership checks
  - Dictionary operations: O(1) average case for defaultdict operations
- **Space complexity**: O(N × L²)
  - `entry_containment` dictionary: Can store up to O(N × L) unique substrings (each cell can contribute up to L substrings of a given length)
  - `cell_substrings` set: O(L) per cell, but this is temporary
  - `results` list: O(N × L) in worst case
  - `unique_matches` dictionary: O(N × L) in worst case

**Dependence on N:**

The execution time is **linearly proportional to N** (the number of entries in the column). This is evident from the algorithm structure:
- The middle loop (line 49) iterates exactly N times: `for cell_value in column`
- Each iteration processes one cell, and the work per cell is independent of N
- The outer loop (substring lengths) and inner loop (positions within cell) are both independent of N

Therefore, if N doubles, the execution time approximately doubles, assuming the average cell length L remains constant. The L³ factor comes from the nested loops over substring lengths and positions, but this is independent of N. In practice, for real-world data where L is typically much smaller than N, the linear dependence on N dominates the overall performance characteristics.

---

### 4. Copy&paste the result of your code using the sample CSV file provided with the exam.

**Run the following command and paste results here:**

```bash
python3 main.py w5-Sample.csv
```

**Results:**

```
CSV: w5-Sample.csv

Column 0:
  "b3" appeared 74 
                      times out of 101 entries

Column 1:
  ". D" appeared 68 
                      times out of 101 entries
  " D" appeared 68 
                      times out of 101 entries
  ". " appeared 100 
                      times out of 101 entries

Column 2:
  (no matches)

Column 3:
  "U@E" appeared 66 
                      times out of 101 entries
  "dio" appeared 66 
                      times out of 101 entries
  "@E" appeared 66 
                      times out of 101 entries
  "U@" appeared 66 
                      times out of 101 entries
  "di" appeared 101 
                      times out of 101 entries
  "io" appeared 66 
                      times out of 101 entries

Column 4:
  "pm dist" appeared 75 
                      times out of 101 entries
  "m dist" appeared 75 
                      times out of 101 entries
  "pm dis" appeared 75 
                      times out of 101 entries
  " dist" appeared 75 
                      times out of 101 entries
  "m dis" appeared 75 
                      times out of 101 entries
  "pm di" appeared 75 
                      times out of 101 entries
  " dis" appeared 75 
                      times out of 101 entries
  "am 1" appeared 75 
                      times out of 101 entries
  "dist" appeared 76 
                      times out of 101 entries
  "m di" appeared 75 
                      times out of 101 entries
  "pm d" appeared 75 
                      times out of 101 entries
  " di" appeared 75 
                      times out of 101 entries
  "am " appeared 100 
                      times out of 101 entries
  "dis" appeared 76 
                      times out of 101 entries
  "ist" appeared 76 
                      times out of 101 entries
  "m 1" appeared 75 
                      times out of 101 entries
  "m d" appeared 75 
                      times out of 101 entries
  "pm " appeared 100 
                      times out of 101 entries
  " 1" appeared 75 
                      times out of 101 entries
  " d" appeared 75 
                      times out of 101 entries
  "am" appeared 101 
                      times out of 101 entries
  "di" appeared 76 
                      times out of 101 entries
  "is" appeared 76 
                      times out of 101 entries
  "m " appeared 100 
                      times out of 101 entries
  "pm" appeared 101 
                      times out of 101 entries
  "st" appeared 76 
                      times out of 101 entries

Column 5:
  (no matches)

Column 6:
  "cof15a3" appeared 71 
                      times out of 101 entries
  "cof15a" appeared 71 
                      times out of 101 entries
  "of15a3" appeared 71 
                      times out of 101 entries
  "cof15" appeared 71 
                      times out of 101 entries
  "f15a3" appeared 71 
                      times out of 101 entries
  "of15a" appeared 71 
                      times out of 101 entries
  "15a3" appeared 71 
                      times out of 101 entries
  "AAA_" appeared 71 
                      times out of 101 entries
  "cof1" appeared 101 
                      times out of 101 entries
  "f15a" appeared 71 
                      times out of 101 entries
  "of15" appeared 71 
                      times out of 101 entries
  "15a" appeared 71 
                      times out of 101 entries
  "5a3" appeared 71 
                      times out of 101 entries
  "AAA" appeared 71 
                      times out of 101 entries
  "AA_" appeared 71 
                      times out of 101 entries
  "cof" appeared 101 
                      times out of 101 entries
  "f15" appeared 71 
                      times out of 101 entries
  "of1" appeared 101 
                      times out of 101 entries
  "15" appeared 71 
                      times out of 101 entries
  "5a" appeared 71 
                      times out of 101 entries
  "AA" appeared 71 
                      times out of 101 entries
  "A_" appeared 71 
                      times out of 101 entries
  "a3" appeared 71 
                      times out of 101 entries
  "co" appeared 101 
                      times out of 101 entries
  "f1" appeared 101 
                      times out of 101 entries
  "of" appeared 101 
                      times out of 101 entries
```

---

### 5. Instructions (assume command line): Steps to follow by an user to go from your code archive to the listed results (copy&paste from the terminal).

**Step-by-step instructions:**

1. Extract the code archive to a directory
2. Open terminal/command prompt
3. Navigate to the project directory:
   ```bash
   cd /path/to/project
   ```
4. Ensure Python 3.10+ is installed:
   ```bash
   python3 --version
   ```
5. Run the program with the sample CSV:
   ```bash
   python3 main.py w5-Sample.csv
   ```
6. For custom parameters:
   ```bash
   python3 main.py w5-Sample.csv -p 60 -m 2
   ```

**Example terminal session:**

```bash
PS C:\Users\rafza\OneDrive\Documents\GitHub\21765 project> python main.py w5-Sample.csv
CSV: w5-Sample.csv

Column 0:
  "b3" appeared 74 
                      times out of 101 entries

Column 1:
  ". D" appeared 68 
                      times out of 101 entries
  " D" appeared 68 
                      times out of 101 entries
  ". " appeared 100 
                      times out of 101 entries

Column 2:
  (no matches)

Column 3:
  "U@E" appeared 66 
                      times out of 101 entries
  "dio" appeared 66 
                      times out of 101 entries
  "@E" appeared 66 
                      times out of 101 entries
  "U@" appeared 66 
                      times out of 101 entries
  "di" appeared 101 
                      times out of 101 entries
  "io" appeared 66 
                      times out of 101 entries

Column 4:
  "pm dist" appeared 75 
                      times out of 101 entries
  "m dist" appeared 75 
                      times out of 101 entries
  "pm dis" appeared 75 
                      times out of 101 entries
  " dist" appeared 75 
                      times out of 101 entries
  "m dis" appeared 75 
                      times out of 101 entries
  "pm di" appeared 75 
                      times out of 101 entries
  " dis" appeared 75 
                      times out of 101 entries
  "am 1" appeared 75 
                      times out of 101 entries
  "dist" appeared 76 
                      times out of 101 entries
  "m di" appeared 75 
                      times out of 101 entries
  "pm d" appeared 75 
                      times out of 101 entries
  " di" appeared 75 
                      times out of 101 entries
  "am " appeared 100 
                      times out of 101 entries
  "dis" appeared 76 
                      times out of 101 entries
  "ist" appeared 76 
                      times out of 101 entries
  "m 1" appeared 75 
                      times out of 101 entries
  "m d" appeared 75 
                      times out of 101 entries
  "pm " appeared 100 
                      times out of 101 entries
  " 1" appeared 75 
                      times out of 101 entries
  " d" appeared 75 
                      times out of 101 entries
  "am" appeared 101 
                      times out of 101 entries
  "di" appeared 76 
                      times out of 101 entries
  "is" appeared 76 
                      times out of 101 entries
  "m " appeared 100 
                      times out of 101 entries
  "pm" appeared 101 
                      times out of 101 entries
  "st" appeared 76 
                      times out of 101 entries

Column 5:
  (no matches)

Column 6:
  "cof15a3" appeared 71 
                      times out of 101 entries
  "cof15a" appeared 71 
                      times out of 101 entries
  "of15a3" appeared 71 
                      times out of 101 entries
  "cof15" appeared 71 
                      times out of 101 entries
  "f15a3" appeared 71 
                      times out of 101 entries
  "of15a" appeared 71 
                      times out of 101 entries
  "15a3" appeared 71 
                      times out of 101 entries
  "AAA_" appeared 71 
                      times out of 101 entries
  "cof1" appeared 101 
                      times out of 101 entries
  "f15a" appeared 71 
                      times out of 101 entries
  "of15" appeared 71 
                      times out of 101 entries
  "15a" appeared 71 
                      times out of 101 entries
  "5a3" appeared 71 
                      times out of 101 entries
  "AAA" appeared 71 
                      times out of 101 entries
  "AA_" appeared 71 
                      times out of 101 entries
  "cof" appeared 101 
                      times out of 101 entries
  "f15" appeared 71 
                      times out of 101 entries
  "of1" appeared 101 
                      times out of 101 entries
  "15" appeared 71 
                      times out of 101 entries
  "5a" appeared 71 
                      times out of 101 entries
  "AA" appeared 71 
                      times out of 101 entries
  "A_" appeared 71 
                      times out of 101 entries
  "a3" appeared 71 
                      times out of 101 entries
  "co" appeared 101 
                      times out of 101 entries
  "f1" appeared 101 
                      times out of 101 entries
  "of" appeared 101 
                      times out of 101 entries

PS C:\Users\rafza\OneDrive\Documents\GitHub\21765 project>
```

---

## Hypothetical parallel implementation: (no need to actually produce a parallel implementation)

Comments about which part of the code is suitable for parallel execution and why. 
What type of partitioning did you consider to use?

**Parallelization Analysis:**

After examining the code structure, I've identified several opportunities for parallelization, each with different trade-offs:

**1. Column-level Parallelization (Most Promising):**

Looking at `kernel.py` lines 30-35, each column is processed independently in a sequential loop. This is an ideal candidate for parallelization because:
- **Independence**: Each column's processing is completely independent - there are no shared data structures or dependencies between columns
- **Coarse-grained**: The work per column is substantial (especially for columns with many entries), so the overhead of parallelization would be minimal
- **Implementation**: We could use Python's `multiprocessing.Pool` or `concurrent.futures` to process columns in parallel. The code would change from:
  ```python
  for column_index in range(len(columns)):
      column_data = columns[column_index]
      column_matches = find_matching_substrings(column_data, threshold, min_len)
  ```
  To something like:
  ```python
  with Pool() as pool:
      results = pool.starmap(process_column, [(col, i, threshold, min_len) for i, col in enumerate(columns)])
  ```
- **Partitioning**: Data partitioning by column - each processor/thread handles a subset of columns
- **Benefit**: If the CSV has C columns and we have P processors, we can theoretically achieve up to min(C, P)× speedup. For the sample file with 7 columns, this could provide significant speedup on a multi-core machine
- **Synchronization**: Minimal - only needed when aggregating final results

**2. Substring Length Parallelization (Moderate Benefit):**

Within `find_matches.py`, the outer loop (line 45) iterates through substring lengths sequentially. These iterations are independent:
- **Independence**: Processing length 2 doesn't depend on length 3, etc. Each length maintains its own `entry_containment` dictionary
- **Implementation**: We could parallelize the loop over `substring_length` using `concurrent.futures` or similar
- **Partitioning**: Task partitioning by substring length - different processors handle different length ranges
- **Challenge**: We'd need to merge results from different lengths, and handle the deduplication step carefully
- **Benefit**: Moderate speedup, but limited by the number of distinct lengths (typically much smaller than N or C)
- **Trade-off**: The overhead of creating threads/processes might outweigh benefits for small datasets, but could help for columns with very long cell values

**3. Cell-level Parallelization (Good for Large N):**

Within the substring length loop, we process cells sequentially (line 49). This could be parallelized:
- **Independence**: Each cell's substring extraction is independent
- **Implementation**: Distribute cells across threads, each thread processes its assigned cells and maintains a local `entry_containment` dictionary, then merge dictionaries
- **Partitioning**: Data partitioning by cell - divide the column's cells across processors
- **Synchronization Challenge**: We need to merge `entry_containment` dictionaries from different threads. Options include:
  - Thread-safe counters (e.g., using locks or atomic operations)
  - Per-thread dictionaries with final merge step
  - Reduce operation to combine results
- **Benefit**: Excellent for large N (many entries per column), as the work scales linearly with N
- **Trade-off**: More complex implementation, and synchronization overhead might reduce benefits for small N

**4. Hybrid Approach (Maximum Parallelism):**

We could combine multiple levels:
- **Level 1**: Process columns in parallel (coarse-grained)
- **Level 2**: Within each column, process substring lengths in parallel (medium-grained)
- **Level 3**: Within each length, process cells in parallel (fine-grained)

This would maximize parallelism but also maximize complexity and overhead. The optimal choice depends on the hardware and data characteristics.

**Recommended Approach:**

For most practical scenarios, I would recommend:
1. **Primary**: Column-level parallelization - This provides the best balance of speedup vs. implementation complexity. It's coarse-grained enough to minimize overhead, and most CSV files have multiple columns that can benefit.
2. **Secondary (if N is very large)**: Within each column, parallelize cell processing - This would help when individual columns have thousands of entries, making the cell-level work substantial enough to justify the synchronization overhead.

**Partitioning Strategy:**

- **Data Partitioning (Recommended)**: Divide the problem by data units (columns or cells). This is natural for this problem because:
  - Each data unit (column/cell) can be processed independently
  - Load balancing is straightforward (distribute columns/cells evenly)
  - Minimal communication needed (only final results)
  
- **Task Partitioning (Alternative)**: Divide by substring lengths. This could work but is less natural because:
  - The number of tasks (lengths) is typically small and variable
  - Load balancing is harder (different lengths may take different amounts of time)
  - Still requires merging results from different lengths

**Implementation Considerations:**

- **Threading vs. Multiprocessing**: For CPU-bound work like string processing, multiprocessing (separate processes) is typically better than threading in Python due to the GIL (Global Interpreter Lock)
- **Memory**: Parallel processing increases memory usage as each process/thread maintains its own data structures
- **I/O**: The data extraction phase reads the file once, so parallelization there wouldn't help. The parallelization benefit comes entirely from the substring matching computation

---

## Credits: (not considered for grading)

List of people (even outside your team) and LLMs who helped you with your work, ordered by how helpful their contribution was (first one was the most helpful).

1. Gabe Pacella - Team member who collaborated on the initial code structure and implementation approach. We worked together to design the module architecture and discussed the algorithm for finding matching substrings.

2. Cursor AI Assistant (Auto) - Helped with code refactoring to differentiate the implementation from reference code, assisted with documentation, and provided guidance on completing the assignment template with detailed technical explanations. 

---

**End of Assignment Template**
