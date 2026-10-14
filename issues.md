# Lab 5 issue table

Line numbers refer to the original vehicle_service.py, preserved in original/.
High-severity Bandit findings are listed first. No medium-severity Bandit
findings were reported. Pylint and Flake8 categories are not Bandit severity levels.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Shell command injection (Bandit B602) | Security, High | 61 | A folder is concatenated into a shell command. Shell metacharacters could execute unintended commands. | Replace subprocess.call with shutil.copy2; the destination is handled as a path. |
| MD5 use (Bandit B324) | Security, High tool rating | 39 | Bandit flags MD5 as a weak security hash. Here it is only used for a short vehicle label. | Use SHA-256 and retain the 8-character display format. This label remains non-unique and unsuitable as a security token. |
| Hardcoded password (Bandit B105) | Security, Low | 8 | A password-like literal is embedded in source, although unused. | Remove the unused constant; no authentication feature depends on it. |
| Subprocess import (Bandit B404) | Security, Low | 3 | Import prompts review of process execution. | Remove the import after replacing the shell-based copy. |
| Mutable default argument (Pylint W0102) | Bug | 12 | history=[] is created once and shared by calls that omit history. | Default to None and create a fresh list for each such call. Explicitly supplied lists still accumulate history. |
| Broad exception (Pylint W0718) | Reliability | 23 | Catching Exception can hide errors unrelated to a missing vehicle. | Catch KeyError only. |
| Missing encoding (Pylint W1514) | Portability | 50 | Saving uses the platform default while loading uses UTF-8. | Specify encoding="utf-8" when saving. |
| Missing module documentation (Pylint C0114) | Documentation | 1 | The module has no description. | Add a module docstring. |
| Missing function documentation (Pylint C0116) | Documentation | 12, 20, 31, 38, 42, 49, 54, 59, 64 | Functions have no docstrings. | Document each function, its behavior and relevant return value. |
| Naming style (Pylint C0103) | Style | 12, 20, 31–34, 38, 42, 49, 54, 59 | Functions, parameters and a local variable use camelCase. | Use snake_case and update every internal call. Use SERVICE_RECORDS for the shared module-level store. |
| Missing comma spacing (Flake8 E231) | Style | 7 | No space follows a comma. | Format the rates dictionary with one entry per line. |
| Missing operator spacing (Flake8 E225) | Style | 43 | best=None has no spaces around =. | Replace the loop with max(..., default=None), retaining first-insertion tie behavior. |
| Missing blank line (Flake8 E302) | Style | 49 | Top-level functions need two separating blank lines. | Add the required blank lines. |
| Long line (Flake8 E501) | Style | 77 | A line is 83 characters long. | Wrap the print call across lines. |

## Additional improvements found by manual review

- Guard main() with `if __name__ == "__main__":` so importing the module does not run the demo or write a file.
- Reject blank/non-string vehicle numbers and unknown service types before changing records. Previously, an unknown service was silently booked at zero cost.
- Simplify the total calculation with sum().

## Verification

| Tool | Before | After |
|---|---|---|
| Pylint 4.1.3 | 4.66/10; 31 messages | 10.00/10; no messages; exit 0 |
| Bandit 1.9.4 | 4 findings: 2 High, 2 Low | No issues; exit 0 |
| Flake8 7.4.1 | 4 findings | No output; exit 0 |

Actual reports are in reports/before and reports/after. No warning suppressions
or disabled checks were used. The demo totals, vehicle count and busiest vehicle
are preserved. The job-card label changes from 353ee89f to bd2cd41f because the
hash algorithm changed. Renamed functions require external callers, if any,
to use the new snake_case names. Eight hexadecimal characters provide only
32 bits and do not guarantee uniqueness; the label still identifies a vehicle,
not each separate booking.
