"""Batch file handlers."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Optional

from season_tool.seasons import (
    compare_country_seasons,
    format_meteorological_season,
    format_traditional_season,
)
from season_tool.temperature import compare_with_city_average, compare_with_perth_average
from season_tool.validation import ValidationError


def process_request_line(line: str) -> Optional[str]:
    """Process one CSV-style request line."""

    stripped = line.strip()
    if not stripped or stripped.startswith("#"):
        return None

    row = next(csv.reader([line]))
    command = row[0].strip().lower() if row else ""

    try:
        if command == "meteorological":
            _require_fields(row, 3)
            return format_meteorological_season(row[1], row[2])

        if command == "traditional":
            _require_fields(row, 3)
            return format_traditional_season(row[1], row[2])

        if command == "compare":
            _require_fields(row, 4)
            comparison = compare_country_seasons(row[1], row[2], row[3])
            return comparison.message

        if command == "temp":
            _require_fields(row, 4)
            comparison = compare_with_city_average(row[1], row[3], row[2])
            return comparison.message

        if command == "perth":
            _require_fields(row, 4)
            comparison = compare_with_perth_average(row[1], row[3], row[2])
            return comparison.message

        return f"ERROR: Unknown command '{row[0]}'."
    except (ValidationError, ValueError, IndexError) as exc:
        return f"ERROR: {exc}"


def process_request_file(input_path: str, output_path: str) -> int:
    """Read request lines and write result lines."""

    source = Path(input_path)
    destination = Path(output_path)
    output_lines = []

    with source.open("r", encoding="utf-8", newline="") as input_file:
        for line_number, line in enumerate(input_file, start=1):
            result = process_request_line(line)
            if result is not None:
                output_lines.append(f"Line {line_number}: {result}")

    with destination.open("w", encoding="utf-8", newline="") as output_file:
        output_file.write("\n".join(output_lines))
        if output_lines:
            output_file.write("\n")

    return len(output_lines)


def _require_fields(row: list[str], expected_count: int) -> None:
    if len(row) != expected_count:
        raise ValueError(
            f"Command '{row[0] if row else ''}' expects {expected_count - 1} fields."
        )
