# ISAD1000/5004 seasons and temperature tool

Python 3 assignment work for ISAD1000/5004 2026 Semester 1.

Student details:

- Name: Austin Delic
- Student ID: 22930121
- Required numeric test data: 121

## Files

All paths below are relative to this submitted folder.

- `README.md` - purpose of the submitted files and run commands.
- `.git/` - local Git repository history for the assignment.
- `.gitignore` - ignores generated Python/cache files.
- `pyproject.toml` - project metadata; no external dependencies are required.
- `code/main.py` - command-line entry point for demo mode, file processing, and repeating interactive use.
- `code/sample_requests.txt` - sample batch input.
- `code/sample_results.txt` - sample batch output.
- `code/season_tool/__init__.py` - package marker for the production modules.
- `code/season_tool/data.py` - season and temperature data tables.
- `code/season_tool/validation.py` - input normalisation and validation.
- `code/season_tool/seasons.py` - season lookup and country comparison logic.
- `code/season_tool/temperature.py` - city and Perth temperature comparison logic.
- `code/season_tool/io_handlers.py` - batch request file processing.
- `code/tests/__init__.py` - package marker for test discovery.
- `code/tests/test_seasons.py` - season black-box and white-box tests.
- `code/tests/test_temperature.py` - temperature black-box and white-box tests.
- `code/tests/test_io_handlers.py` - file input/output tests.
- `code/tests/test_main.py` - command-line and interactive console tests.
- `documents/22930121_Austin_Delic_ISE2026S1.md` - markdown report.
- `documents/22930121_Austin_Delic_ISE2026S1.pdf` - PDF report.
- `documents/screenshots/production_demo.png` - production demo screenshot.
- `documents/screenshots/batch_file_run.png` - batch mode screenshot.
- `documents/screenshots/test_execution.png` - unit test execution screenshot.
- `documents/screenshots/git_log.png` - Git log screenshot.
- The branch and commit plan is inside the report's Version Control section.

## Run production code

```bash
python3 code/main.py --demo
python3 code/main.py --file code/sample_requests.txt code/sample_results.txt
python3 code/main.py
```

## Run tests

```bash
python3 -m unittest discover -s code/tests -t code -v
```

## Submission checklist

- Folder name for Blackboard zip: `22930121_Austin_Delic_ISE2026S1_Assignment`
- The folder contains `code/`, `documents/`, `README.md`, `pyproject.toml`, and `.git/`.
- The markdown report, PDF report, and screenshot evidence are in `documents/`.
