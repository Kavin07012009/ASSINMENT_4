# Python Programming Assignment 4 CO4

**Student:** [Enter full name]  
**Register number:** [Enter register number]  
**GitHub repository:** [Paste the repository URL here]  
**Python used for execution evidence:** Python 3.14.7  
**Libraries:** Python standard library only

This report covers all six assignment tasks. Programs, sample files, generated reports and captured output are in the matching task folders. Measurements are from Python 3.14.7 on this machine and can vary on another computer.

## Task 1 File-processing design review

### 1.1 Script deficiencies and office impact

| Deficiency | What could go wrong |
|---|---|
| Hard-coded desktop path | The script fails for another staff account, computer, or month. |
| `open()` has no `with` | An exception can bypass `close()`, leaving a handle open until cleanup. |
| `read()` loads everything | Memory grows with the whole file; large monthly files use unnecessary memory. |
| Bare `except: pass` | Permission errors, programming mistakes, and bad records disappear without explanation. |
| `int()` parses money | A valid amount such as 1250.50 raises `ValueError` and is silently lost. |
| Repeated `report + text` | Strings are immutable; repeated copying can waste time for a large report. |
| `split("\n")` creates an empty last record | A trailing newline creates an empty row; the broad handler hides it as if it were an error. |
| Rejected lines are not recorded | The office cannot correct missing or malformed student bills, so totals may be incomplete. |
| Amount formatting is absent | Paise and whole rupees may appear inconsistently in the report. |

The repaired `Task1/mess_bill.py` takes the source and report filenames as parameters. It opens both with `with`, reads one line at a time, uses `Decimal` for exact paise, skips blank lines, and retains rejected rows with their line numbers and reasons. The accepted report is written line by line instead of being built with repeated `+` or stored in a second full-sized string.

### 1.2 Alternative and complexity

For n lines, iterating and `read()`/`readlines()` both take O(n) time. `read()` stores the whole input string; `readlines()` stores the list of all lines, so both need O(file size) input memory. Iteration needs O(one line) input memory, plus O(r) for the required rejected-line list of r bad rows. The repaired report is streamed to its destination file. With 50,000 records, this bounds working memory while preserving an audit trail.

### 1.3 Design defence (under 100 words)

The repair uses one open context per file, parses each line as it arrives and writes accepted rows directly to the report. Decimal preserves cents exactly. Specific validation records bad rows instead of hiding them, and blank trailing lines are ignored. Input memory stays near one line, apart from the rejected-line audit list. The total and output file still grow as required, but the program does not keep a second copy of the complete input or repeatedly copy an expanding report string. This is safer for 50,000 records and easier to audit.

## Task 2 From requirement to file-processing design

### 2.1 Data model and output files

Input is UTF-8 text, one record per line: `register,date,status`, where status is `P` or `A`. A dictionary maps each register number to present count, absent count, and dated status entries. The output files are `attendance_percentages.csv` (all students, counts and percentage), `below_75.csv` (students below 75%), and `damaged_lines.csv` (filename, line number and error reason). The third file is the audit log required by the prompt.

### 2.2 File operations

The processor uses `pathlib.Path.glob("*.csv")` to list daily files. It validates ISO dates with `datetime.date.fromisoformat()` and catches malformed date values before counting them. It opens inputs in `r` mode and UTF-8, iterates by line instead of calling `read()` so it can report exact line numbers, and writes fresh reports in `w` mode using `csv.writer` and UTF-8. Output reports are rebuilt each run, so append mode is not appropriate. `with` closes each file even when decoding or parsing fails.

### 2.3 Monthly processing pseudocode

```text
BEGIN PROCESS_MONTH(input_folder, output_folder)
    SET attendance_counts TO empty dictionary
    SET damaged_rows TO empty list
    FOR EACH path IN sorted CSV files in input_folder
        TRY
            OPEN path FOR reading with UTF-8
            FOR EACH line WITH line_number
                SPLIT line into register, date, status
                IF fields are missing or status is not P or A THEN
                    APPEND (path name, line_number, reason) to damaged_rows
                    CONTINUE
                END IF
                INCREMENT present or absent count for register
                STORE date and status for register
            END FOR
        CATCH file or decoding error
            APPEND file-level error to damaged_rows
        END TRY
    END FOR
    WRITE all percentages to attendance_percentages.csv
    WRITE students below 75 percent to below_75.csv
    WRITE damaged_rows to damaged_lines.csv
END PROCESS_MONTH
```

### 2.4 Trace

For `day1.csv`, line 1 increments 192311001 present to 1; line 2 increments 192311002 absent to 1; line 3 has only two fields, so it is added to the damaged log as `(day1.csv, 3, malformed attendance record)` and does not change any count. The completed sample writes two student percentages and two damaged rows across the two input files.

Re-reading all f files for each of s students and scanning l lines per file takes O(s·f·l) time. Reading every file once and accumulating counts takes O(f·l) average time, with O(s) count storage plus error records. Re-reading can use less accumulated memory if outputs are streamed one student at a time, but it repeats I/O and parsing.

## Task 3 Design the error handling

### 3.1 Failure table

| Failure | Typical built-in exception or handling |
|---|---|
| Missing input folder/file | `FileNotFoundError` (or an empty file list if folder discovery finds nothing) |
| No permission to read | `PermissionError`, a subtype of `OSError` |
| Wrong UTF-8 bytes | `UnicodeDecodeError` |
| Damaged fields/status/date | Custom `InvalidRecord`; `datetime.date.fromisoformat()` raises `ValueError`, wrapped as `InvalidRecord` |
| Indexing a missing field | `IndexError`; avoided by validating the field count before indexing |
| Empty file | No exception; zero valid rows and zero damaged rows |
| Path points to directory | `IsADirectoryError`, a subtype of `OSError` |
| Output cannot be written | `PermissionError` or another `OSError` |

### 3.2 Custom exception and complete try statement

`InvalidRecord` is raised in `parse_line()` when field count, required fields, or status fail. `summarise()` catches that error per line and records `(line number, reason)`, allowing the rest of the file to continue. File-level exceptions are converted to `AttendanceFileError` with `raise ... from exc`; the caller can inspect `__cause__` to find the original `FileNotFoundError`, `PermissionError`, or `UnicodeDecodeError`. Its `else` returns the completed counts only after successful reading, and `finally` records that the read attempt ended. The output shows the assignment example `(1, 1, [(3, 'expected 3 fields, found 2'), (4, "invalid status 'L'")])` and handles a missing filename without terminating the task.

### 3.3 Misuse experiment and alternative

`broad_except_pass_demo()` intentionally refers to `attendance_total` after assigning the misspelled `attendence_total`. The `NameError` is swallowed by `except Exception: pass`, so the output remains `not set` with no explanation. This demonstrates why broad handlers erase evidence of bugs.

The look-before-you-leap alternative checks delimiter count, required fields and status before constructing a record. Both approaches are O(1) per fixed-width line, or O(total characters) including parsing. With rare invalid rows, exception-based validation keeps the normal path direct; with frequent bad rows, raising and catching an exception on every row adds overhead, so explicit checks are typically preferable. Specific exception handling is still needed for file and encoding failures.

## Task 4 File and exception forensics

The defective `save_returns()` opens the log in `w` mode on every day, so each run truncates the earlier days. It writes each title without a newline, joining titles together. If `write()` fails, the next `close()` is skipped and no error log is written; the file object may remain open until it is reclaimed. `process()` catches only missing input files, so write failures are not reported.

The three-day test produces the defective value `'The Odyssey'`: the first two days were overwritten, and book names were concatenated before that. The repaired function opens the destination in append mode, writes `book + newline`, and uses `with` for both input and output. It appends write and missing-file errors to `errors.log`; the sample shows all four returned titles on separate lines, and an injected `TypeError` is recorded before it is re-raised.

Two prevention rules are: (1) use context managers for every file handle; (2) choose `w` only for a complete replacement report and `a` for a cumulative log, and always add record separators. Manual `try/finally` that reliably closes each file has the same O(n) time and O(1) extra working space as `with`. Both leave zero files open after the cleanup block. Manual closing without a `finally` can leave one handle open per failing path; `with` closes it automatically.

## Task 5 The same utility organised four ways

All four variants read the same attendance sample and produce the same summary and three-consecutive-day report. Their output identifies 192311001 as having three consecutive absences. The required second report affected these files in the designs: one script **1**; one imported module plus main **1** (the utility module); three modules **2** (`stats.py` and `report.py`); package **2** (`attendance/stats.py` and `attendance/report.py`). These counts refer to the files that contain the calculation and output behavior; the main orchestration did not change.

| Organisation | Readability and reuse | Testing and naming |
|---|---|---|
| One script | Easiest to start; all concerns are together and reuse is weak. | Simple to run; harder to isolate reader/statistics tests. |
| One module + main | Reusable functions, but unrelated responsibilities remain in one imported file. | Main can be tested separately; generic module names can collide. |
| Three modules | Reader, statistics and report responsibilities are clear. | Each module can be tested independently; imports are simple within the project. |
| `attendance` package | Best structure as the project grows; package exposes a small public interface. | Clear qualified names and isolated tests; one-time organization has extra setup. |

`import attendance.stats` binds the top-level package name `attendance`, so call `attendance.stats.percentage(...)`. `from attendance import stats` binds the submodule as `stats`, so call `stats.percentage(...)`. `from attendance.stats import percentage` binds the function directly and calls `percentage(...)`; this is concise but can make name collisions less obvious. The package run prints that the first two references resolve to the same module and that `percentage(3,4)` is 75.0.

A one-script alternative needs no package layout and is adequate for a small utility. Importing a package adds a one-time module load; Python caches loaded modules in `sys.modules`, so later imports reuse them. Package memory is proportional to the imported module code and objects, not the number of attendance records. Finding and changing a function is quickest in a single file only when it is short; separated modules make responsibility clearer as more functions are added.

## Task 6 College fest registration design challenge

### Stage 1 Requirements

Inputs are five department CSV files with register, name, department, e-mail, and semicolon-separated events. Outputs are a deduplicated master CSV, one participant CSV per event, a summary text file, and an error CSV. Requirements are testable: valid rows must appear in the master; a repeated register number must appear once with the union of its events; each valid event selection must appear once in its participant file; invalid e-mails and malformed rows must be logged with source and line; a missing department file must be logged while the other files still process.

Records are considered duplicates by case-insensitive register number. The first accepted name, department and e-mail are retained, and later event sets are unioned. The e-mail check uses string methods: exactly one `@`, nonempty local/domain parts, no whitespace, and a dot inside the domain that is not at either end. This is a simple assignment-level check, not a complete e-mail standards validator.

### Stage 2 Flow

```text
Department input files → line reader → field/e-mail validation
       │                       │ valid                    └ invalid → error log
       │                       ↓
       │              duplicate register check (set/dictionary)
       │                       ↓
       └─ missing file → error log     merge event sets
                                       ↓
                master CSV + event participant CSVs + summary + errors
```

### Stage 3 Package and processing pseudocode

Package structure: `fest/reader.py` reads and validates one department; `fest/merge.py` deduplicates and unions events; `fest/reports.py` writes all outputs; `fest/processor.py` continues across files and coordinates the stages; `fest/benchmark.py` compares set-based and list-search duplicate checks; `fest/main.py` runs the demonstration.

```text
BEGIN PROCESS_FEST(input_folder, output_folder, department_names)
    SET valid_records TO empty list
    SET errors TO empty list
    FOR EACH department IN department_names
        TRY
            OPEN department file as UTF-8 text
            FOR EACH line WITH line_number
                TRY
                    SPLIT into five fields and event list
                    IF fields are invalid OR email check fails THEN RAISE InvalidRegistration
                    APPEND validated record to valid_records
                CATCH InvalidRegistration
                    APPEND filename, line_number and reason to errors
                END TRY
            END FOR
        CATCH missing, permission, decoding or other file error
            APPEND filename, line 0 and reason to errors
            CONTINUE WITH next department
        END TRY
    END FOR
    SET master TO dictionary keyed by normalized register number
    MERGE duplicate event sets into existing master records
    WRITE master, one file per event, summary and errors
END PROCESS_FEST
```

### Stage 4 Demonstration and measurements

The sample includes a duplicate Asha registration with different phone-like e-mail text and additional events, an invalid e-mail, a damaged row, and a missing Management file. The result contains seven unique master entries and merges the duplicate's three event choices. The error file records the invalid e-mail at Science line 2, the malformed record at Commerce line 2, and the absent Management file at line 0. The program continues and writes every output.

| Registrations | Set-based pass (s) | List-search pass (s) | List comparisons | List-search estimate (s) |
|---:|---:|---:|---:|---:|
| 1,000 | 0.000029 | 0.004697 | 499,500 | 0.0047 measured |
| 100,000 | 0.003540 | Not run | 4,999,950,000 worst-case | 47.0 extrapolated |

With n unique registrations, list search compares each new register with all earlier ones, for n(n−1)/2 comparisons and O(n²) time. The 100,000-record estimate scales the measured 1,000-record list scan; it is explicitly not an executed timing. A set/dictionary membership check is O(1) average, so the pass is O(n) average and uses O(n) space. The measured set implementation handled 100,000 distinct registrations in 0.003540 seconds. A set is the right deployment choice for detecting duplicates while preserving the first accepted record in a companion dictionary.

## Submission checklist

The assignment repository name is `CSA08-[RegisterNumber]-Assignment4`. Add personal details and the real GitHub URL to the cover page and README, commit task folders progressively, and share the repository with the faculty. Add code execution screenshots to each task if required; the package currently includes text run captures. Submit the PDF to the required course portals yourself.
