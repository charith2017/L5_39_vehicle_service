# Lab 5 suggested reflection answers

The supplied README requests four reflection answers, but the uploaded handout
does not contain the questions. The four topics below are suggested preparation
answers, not a claim that these are the exact assigned questions. Adjust them
if your instructor provides a separate question sheet.

## 1. What does each static analysis tool check?

Pylint checks code quality and common programming mistakes. In this program,
it found the shared default list, broad exception handler, missing encoding,
and naming/documentation problems. Bandit checks security patterns and found
shell execution, MD5, a hardcoded password and the subprocess import. Flake8
checks style and reported whitespace, blank-line and line-length problems.

## 2. Which problems should be fixed first and why?

The unsafe shell command should be fixed first because a crafted destination
could run an unintended command. shutil.copy2 copies the file without a shell.
Bandit also rated MD5 High, so it was replaced with SHA-256. However, the actual
context matters: the value is a short display label, not a password or security
token. The mutable default list is also important because unrelated bookings
can unexpectedly share history. Using None gives each default call a fresh list.

## 3. How can the fixes be verified?

Rerun all three tools and compare their reports. The cleaned file achieved
10.00/10 in Pylint, zero Bandit findings and no Flake8 output. Run the demo as
well: its totals remain 2300 and 2500, with three vehicles on file and
KA01AB1234 as the busiest vehicle. The job-card value changes because its hash
algorithm changed. Focused runtime checks also verify independent histories,
cancellation, JSON round trips, backup paths and safe importing.

## 4. What are the benefits and limitations of static analysis?

Static analysis finds many problems before the program is run and encourages
consistent, readable code. The tools complement each other because they check
different types of issues. They cannot prove that the program is correct or
secure. For example, a short hash can still collide even after the MD5 warning
is fixed, and tool checks alone do not establish whether business rules are
correct. Review the code and run meaningful functional checks as well.
