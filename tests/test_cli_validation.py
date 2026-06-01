import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = REPO_ROOT / "examples" / "validation"
ALS_PATH = EXAMPLES_DIR / "RYM_2026-03.als"
LOCATORS_SCRIPT = REPO_ROOT / "src" / "extract_locators.py"
TIMELINE_SCRIPT = REPO_ROOT / "src" / "extract_timeline.py"


class CliValidationTests(unittest.TestCase):
    """
    End-to-end CLI checks against the canonical validation ALS file.

    These tests intentionally use the command-line scripts instead of importing
    private functions. That makes them slower than unit tests, but it verifies
    the exact workflow users run: argument parsing, file writing, exit codes,
    and fixture-compatible output.
    """

    def run_cli(self, *args, check=True):
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"

        result = subprocess.run(
            ["python3", *map(str, args)],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )

        if check and result.returncode != 0:
            self.fail(
                "Command failed with exit code "
                f"{result.returncode}:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
            )

        return result

    def assert_files_match(self, expected_path, actual_path):
        expected = Path(expected_path).read_text(encoding="utf-8")
        actual = Path(actual_path).read_text(encoding="utf-8")
        self.assertEqual(actual, expected)

    def test_extract_locators_highres_fixtures_match(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            actual_tsv = temp_path / "RYM_2026-03_locators_highres.tsv"
            actual_mixcloud = temp_path / "RYM_2026-03_mixcloud_highres.txt"

            self.run_cli(
                LOCATORS_SCRIPT,
                ALS_PATH,
                "--precision=3",
                "--output",
                actual_tsv,
                "--mixcloud",
                actual_mixcloud,
                "--time-header=Time",
                "--label-header=Title",
                "--add-offset=27",
            )

            self.assert_files_match(
                EXAMPLES_DIR / "RYM_2026-03_locators_highres.tsv",
                actual_tsv,
            )
            self.assert_files_match(
                EXAMPLES_DIR / "RYM_2026-03_mixcloud_highres.txt",
                actual_mixcloud,
            )

    def test_extract_locators_metadata_fixtures_match(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            actual_tsv = temp_path / "RYM_2026-03_locators_metadata.tsv"
            actual_json = temp_path / "RYM_2026-03_locators_metadata.json"

            self.run_cli(
                LOCATORS_SCRIPT,
                ALS_PATH,
                "--add-offset=27",
                "--columns=all",
                "--output",
                actual_tsv,
                "--json",
                actual_json,
                "--json-format=pretty",
            )

            self.assert_files_match(
                EXAMPLES_DIR / "RYM_2026-03_locators_metadata.tsv",
                actual_tsv,
            )

            expected = json.loads(
                (EXAMPLES_DIR / "RYM_2026-03_locators_metadata.json").read_text(
                    encoding="utf-8"
                )
            )
            actual = json.loads(actual_json.read_text(encoding="utf-8"))

            # The fixture records the absolute path from the machine that
            # generated it. The script version also changes as releases are
            # cut. Normalize both fields so clones in other locations can still
            # verify the semantic JSON output.
            expected["version"] = "<normalized>"
            actual["version"] = "<normalized>"
            expected["source_file"] = "<normalized>"
            actual["source_file"] = "<normalized>"
            self.assertEqual(actual, expected)

    def test_timeline_locator_rows_match_locator_metadata(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            actual_tsv = Path(temp_dir) / "RYM_2026-03.timeline-locators.tsv"

            self.run_cli(
                TIMELINE_SCRIPT,
                ALS_PATH,
                "--precision=3",
                "--event-types=locator",
                "--columns=wall_seconds,name,event_id,absolute_beats",
                "--output",
                actual_tsv,
            )

            metadata_rows = [
                line.rstrip("\n").split("\t")
                for line in (EXAMPLES_DIR / "RYM_2026-03_locators_metadata.tsv")
                .read_text(encoding="utf-8")
                .splitlines()
            ]
            timeline_rows = [
                line.rstrip("\n").split("\t")
                for line in actual_tsv.read_text(encoding="utf-8").splitlines()
            ]

            expected_rows = [["Wall Seconds", "Name", "Event ID", "Absolute Beats"]]

            for row in metadata_rows[1:]:
                expected_rows.append([row[5], row[1], row[10], row[7]])

            self.assertEqual(timeline_rows, expected_rows)

    def test_missing_input_returns_error_exit_code(self):
        missing_file = REPO_ROOT / "examples" / "validation" / "missing.als"

        locator_result = self.run_cli(
            LOCATORS_SCRIPT,
            missing_file,
            "--output",
            Path(tempfile.gettempdir()) / "missing-locators.tsv",
            check=False,
        )
        timeline_result = self.run_cli(
            TIMELINE_SCRIPT,
            missing_file,
            "--output",
            Path(tempfile.gettempdir()) / "missing-timeline.tsv",
            check=False,
        )

        self.assertEqual(locator_result.returncode, 1)
        self.assertIn("status     error", locator_result.stderr)
        self.assertEqual(timeline_result.returncode, 1)
        self.assertIn("status     error", timeline_result.stderr)


if __name__ == "__main__":
    unittest.main()
