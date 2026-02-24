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

1. **CSV Format**: The CSV file uses standard comma-separated format. Empty rows are skipped, and cells may contain any characters including spaces, symbols, and special characters. Cells are trimmed of leading/trailing whitespace.

2. **Substring Matching**: A substring "appears in" an entry if it exists anywhere within that entry's text (not necessarily as a complete word). Each unique substring within a cell is counted only once per cell, even if it appears multiple times in that cell.

3. **Threshold Calculation**: The percentage threshold (default 60%) is applied per column independently. The minimum count is calculated as `max(1, int(threshold * N))` where N is the number of entries in the column, ensuring at least one entry must contain the substring.

4. **Output Format**: Results are sorted by substring length (longest first), then alphabetically. All substrings of length ≥ min_len (default 2) that meet the threshold are reported, including overlapping substrings and substrings that are prefixes/suffixes of longer matches. 

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
- Input: `csv_path: str`, `threshold: float`, `min_len: int`
- Output: `list[tuple[int, int, list[tuple[str, int]]]]` - (column_index, total_entries, matches)

**Kernel Module → Data Extraction Module:**
- Input: `filepath: str`
- Output: `list[list[str]]` - List of columns, each column is a list of cell values

**Kernel Module → Find Matches Module:**
- Input: `column: list[str]`, `threshold: float`, `min_len: int`
- Output: `list[tuple[str, int]]` - List of (substring, count) tuples

---

### 2. Which modules should be optimized to increase the sequential execution speed? Present your thoughts about this subject, no implementation needed.

**Your analysis here:**

1. **Find Matches Module** - This is the computational bottleneck:
   - Currently iterates through all substring lengths from min_len to max_len
   - For each length, scans all cells and extracts all substrings
   - Time complexity: O(N × L³) where N = number of entries, L = average length
   - Could be optimized by:
     - Early termination when no matches found at a length
     - Using more efficient data structures
     - Reducing redundant substring extraction

2. **Data Extraction Module** - Minor optimization potential:
   - Currently reads entire file into memory
   - For very large files, could use streaming
   - But for typical CSV sizes, current approach is fine

3. **Kernel Module** - Minimal optimization needed:
   - Just orchestrates calls, minimal computation

---

### 3. Briefly describe the algorithm for finding matches.
If a data column has N lines, how do you expect the execution time to depend on N?

**Algorithm Description:**

1. Calculate minimum count: `min_count = max(1, int(threshold * N))`
2. Find maximum cell length in the column
3. For each substring length from `min_len` to `max_len`:
   - Initialize a dictionary to count substring occurrences
   - For each cell in the column:
     - Extract all substrings of current length
     - Track unique substrings per cell (avoid double-counting)
     - Increment count for each unique substring found
   - Collect substrings that appear in at least `min_count` entries
4. Deduplicate results (same substring may qualify at multiple lengths)
5. Sort by length (longest first), then alphabetically

**Time Complexity Analysis:**

For a column with N entries and average cell length L:
- **Time complexity**: O(N × L³)
  - Outer loop: O(L) iterations (lengths from min_len to max_len)
  - Middle loop: O(N) iterations (cells)
  - Inner loop: O(L) iterations (substring positions)
  - Substring extraction: O(L) per substring
- **Space complexity**: O(N × L²) for storing substring counts

**Dependence on N:**
- Execution time is **linearly proportional to N** (number of entries)
- As N doubles, execution time approximately doubles
- The L³ factor (related to string lengths) is independent of N

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

**1. Column-level Parallelization:**
- **Suitable**: Yes - Each column can be processed independently
- **Partitioning**: Data partitioning by column
- **Implementation**: Process each column in parallel using separate threads/processes
- **Benefit**: If CSV has C columns, can achieve up to C× speedup (limited by cores)

**2. Substring Length Parallelization:**
- **Suitable**: Yes - Different substring lengths can be processed in parallel
- **Partitioning**: Task partitioning by substring length
- **Implementation**: Process different lengths concurrently
- **Benefit**: Moderate speedup, but limited by number of lengths

**3. Cell-level Parallelization:**
- **Suitable**: Partially - Can parallelize substring extraction within a column
- **Partitioning**: Data partitioning by cell
- **Implementation**: Distribute cells across threads, aggregate results
- **Benefit**: Good for large N, but requires synchronization for counting

**Recommended Approach:**
- **Primary**: Column-level parallelization (coarse-grained, minimal synchronization)
- **Secondary**: Within each column, parallelize substring extraction across cells
- **Data Structure**: Use thread-safe counters or reduce operations

**Partitioning Type:**
- **Data Partitioning**: Divide columns or cells across processors
- **Task Partitioning**: Divide substring length iterations across processors
- **Hybrid**: Combine both approaches for maximum parallelism

---

## Credits: (not considered for grading)

List of people (even outside your team) and LLMs who helped you with your work, ordered by how helpful their contribution was (first one was the most helpful).

1. Gabe Pacella (team member - collaborated on code structure and implementation)
2. Auto (Cursor AI assistant - helped with code implementation, documentation, and assignment completion) 

---

**End of Assignment Template**
