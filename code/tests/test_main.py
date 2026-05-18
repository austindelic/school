"""Tests for command-line interface paths."""

import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import main as cli


def input_side_effect(values):
    inputs = iter(values)

    def fake_input(prompt=""):
        print(prompt, end="")
        return next(inputs)

    return fake_input


class MainCliTests(unittest.TestCase):
    def test_main_demo_branch_prints_demo_output(self):
        output = io.StringIO()

        with patch.object(sys, "argv", ["main.py", "--demo"]):
            with redirect_stdout(output):
                cli.main()

        text = output.getvalue()
        self.assertIn("Season and temperature learning tool demo", text)
        self.assertIn("Australia in January: Summer", text)
        self.assertNotIn("Do you want to ask something else?", text)

    def test_main_file_branch_processes_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            source = Path(temp_dir) / "requests.txt"
            destination = Path(temp_dir) / "results.txt"
            source.write_text("meteorological,Australia,January\n", encoding="utf-8")
            output = io.StringIO()

            with patch.object(
                sys,
                "argv",
                ["main.py", "--file", str(source), str(destination)],
            ):
                with redirect_stdout(output):
                    cli.main()

            self.assertIn("Processed 1 request lines.", output.getvalue())
            self.assertNotIn(
                "Do you want to ask something else?", output.getvalue()
            )
            self.assertIn(
                "The meteorological season in Australia in January is Summer.",
                destination.read_text(encoding="utf-8"),
            )

    def test_interactive_unknown_option_path(self):
        output = io.StringIO()

        with patch("builtins.input", side_effect=input_side_effect(["9", "n"])):
            with redirect_stdout(output):
                cli.run_interactive()

        self.assertIn("Unknown option.", output.getvalue())
        self.assertIn("Do you want to ask something else? (y/n):", output.getvalue())

    def test_interactive_validation_error_path(self):
        output = io.StringIO()

        with patch(
            "builtins.input",
            side_effect=input_side_effect(["1", "Canada", "March", "n"]),
        ):
            with redirect_stdout(output):
                cli.run_interactive()

        self.assertIn("Error: Unsupported country 'Canada'", output.getvalue())
        self.assertIn("Do you want to ask something else? (y/n):", output.getvalue())

    def test_interactive_can_run_another_request(self):
        output = io.StringIO()

        with patch(
            "builtins.input",
            side_effect=input_side_effect(
                ["1", "Australia", "January", "y", "2", "August", "n"]
            ),
        ):
            with redirect_stdout(output):
                cli.run_interactive()

        text = output.getvalue()
        self.assertIn("Summer", text)
        self.assertIn("The traditional season in Australia in August is Djilba.", text)
        self.assertEqual(text.count("Do you want to ask something else? (y/n):"), 2)

    def test_interactive_compare_is_meteorological_only(self):
        output = io.StringIO()

        with patch(
            "builtins.input",
            side_effect=input_side_effect(["3", "Australia", "Japan", "January", "n"]),
        ):
            with redirect_stdout(output):
                cli.run_interactive()

        text = output.getvalue()
        self.assertIn("different meteorological seasons", text)
        self.assertNotIn("Season type", text)


if __name__ == "__main__":
    unittest.main()
