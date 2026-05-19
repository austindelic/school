"""Tests for batch request handling."""

import tempfile
import unittest
from pathlib import Path

from season_tool.io_handlers import process_request_file, process_request_line


class FileHandlerTests(unittest.TestCase):
    def test_blank_and_comment_lines_are_skipped(self):
        self.assertIsNone(process_request_line(""))
        self.assertIsNone(process_request_line("# comment"))

    def test_meteorological_request_line(self):
        result = process_request_line("meteorological,Australia,January")
        self.assertEqual(
            result, "The meteorological season in Australia in January is Summer."
        )

    def test_traditional_request_line(self):
        result = process_request_line("traditional,Australia,August")
        self.assertEqual(
            result, "The traditional season in Australia in August is Djilba."
        )

    def test_traditional_request_rejects_non_australia(self):
        result = process_request_line("traditional,Spain,January")
        self.assertEqual(
            result, "ERROR: Traditional season data is only available for Australia."
        )

    def test_compare_request_line(self):
        result = process_request_line("compare,Malaysia,Sri Lanka,July")
        assert result is not None
        self.assertIn("same meteorological season", result)

    def test_compare_request_rejects_old_extra_field_format(self):
        result = process_request_line("compare,Malaysia,Sri Lanka,July,meteorological")
        self.assertEqual(result, "ERROR: Command 'compare' expects 3 fields.")

    def test_temperature_request_line(self):
        result = process_request_line("temp,Perth,Evening,29.0")
        assert result is not None
        self.assertIn("Perth's afternoon average", result)
        self.assertIn("by 6.0C", result)
        self.assertNotIn("The difference is more than 6.0C.", result)

    def test_perth_request_line(self):
        result = process_request_line("perth,Brisbane,Morning,31.0")
        assert result is not None
        self.assertIn("Perth's morning average", result)
        self.assertIn("The difference is more than 6.0C.", result)

    def test_unknown_command_reports_error(self):
        result = process_request_line("unknown,Australia,January")
        self.assertEqual(result, "ERROR: Unknown command 'unknown'.")

    def test_validation_error_is_written_as_error(self):
        result = process_request_line("meteorological,Canada,March")
        assert result is not None
        self.assertTrue(result.startswith("ERROR: Unsupported country 'Canada'"))

    def test_process_request_file_writes_results(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "requests.txt"
            output = Path(temp_dir) / "results.txt"
            source.write_text(
                "\n".join(
                    [
                        "# skip",
                        "meteorological,Australia,January",
                        "temp,Adelaide,Morning,121",
                    ]
                ),
                encoding="utf-8",
            )

            processed = process_request_file(str(source), str(output))

            self.assertEqual(processed, 2)
            content = output.read_text(encoding="utf-8")
            self.assertIn("Line 2: The meteorological season", content)
            self.assertIn("Line 3: ERROR: Temperature 121.0C", content)


if __name__ == "__main__":
    unittest.main()
