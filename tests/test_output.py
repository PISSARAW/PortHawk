"""
test_output.py — Tests for porthawk.output.


"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from porthawk.output import write_csv, write_json


SAMPLE_RESULTS = [
    {"port": 22, "state": "open", "banner": "SSH-2.0-OpenSSH_9.0"},
    {"port": 80, "state": "open", "banner": None},
    {"port": 443, "state": "closed", "banner": None},
]


class TestWriteJson:
    """Unit tests for :func:`porthawk.output.write_json`."""

    def test_creates_valid_json_file(self, tmp_path: Path):
        """Output must be a valid JSON file containing all results."""
        json_file = tmp_path / "results.json"
        write_json(SAMPLE_RESULTS, json_file)

        assert json_file.exists()
        with json_file.open("r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        assert loaded_data == SAMPLE_RESULTS

    def test_creates_parent_directories(self, tmp_path: Path):
        """Parent directories must be created if they do not exist."""
        json_file = tmp_path / "nested" / "json" / "results.json"
        write_json(SAMPLE_RESULTS, json_file)

        assert json_file.exists()
        assert json_file.parent.is_dir()

    def test_json_is_pretty_printed(self, tmp_path: Path):
        """JSON must be indented (pretty-printed), not minified."""
        json_file = tmp_path / "results.json"
        write_json(SAMPLE_RESULTS, json_file)

        with json_file.open("r", encoding="utf-8") as f:
            content = f.read()
        assert "\n" in content and "    " in content

    def test_accepts_string_filepath(self, tmp_path: Path):
        """The writer must accept both Path and str for the destination."""
        json_file = tmp_path / "as-string.json"
        write_json(SAMPLE_RESULTS, str(json_file))
        assert json_file.exists()

    def test_raises_on_empty_results(self, tmp_path: Path):
        """Passing an empty list must raise ValueError."""
        json_file = tmp_path / "results.json"
        with pytest.raises(ValueError):
            write_json([], json_file)


class TestWriteCsv:
    """Unit tests for :func:`porthawk.output.write_csv`."""

    def test_creates_csv_with_header(self, tmp_path: Path):
        """Output must be a CSV file with a header row."""
        csv_file = tmp_path / "results.csv"
        write_csv(SAMPLE_RESULTS, csv_file)

        assert csv_file.exists()
        with csv_file.open("r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            assert header == ["port", "state", "banner"]

    def test_csv_row_count_matches_results(self, tmp_path: Path):
        """CSV must have exactly len(results) data rows (excluding header)."""
        csv_file = tmp_path / "results.csv"
        write_csv(SAMPLE_RESULTS, csv_file)

        with csv_file.open("r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            rows = list(reader)
        assert len(rows) == len(SAMPLE_RESULTS)

    def test_csv_rows_match_result_values(self, tmp_path: Path):
        """CSV rows must preserve values and serialize None as an empty field."""
        csv_file = tmp_path / "results.csv"
        write_csv(SAMPLE_RESULTS, csv_file)

        with csv_file.open("r", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))

        assert rows[0] == {
            "port": "22",
            "state": "open",
            "banner": "SSH-2.0-OpenSSH_9.0",
        }
        assert rows[1] == {"port": "80", "state": "open", "banner": ""}
        assert rows[2] == {"port": "443", "state": "closed", "banner": ""}

    def test_raises_on_empty_results(self, tmp_path: Path):
        """Passing an empty list must raise ValueError."""
        csv_file = tmp_path / "results.csv"
        with pytest.raises(ValueError):
            write_csv([], csv_file)

    def test_creates_parent_directories(self, tmp_path: Path):
        """Parent directories must be created if they do not exist."""
        csv_file = tmp_path / "nested" / "csv" / "results.csv"
        write_csv(SAMPLE_RESULTS, csv_file)

        assert csv_file.exists()
        assert csv_file.parent.is_dir()

    def test_accepts_string_filepath(self, tmp_path: Path):
        """The writer must accept both Path and str for the destination."""
        csv_file = tmp_path / "as-string.csv"
        write_csv(SAMPLE_RESULTS, str(csv_file))
        assert csv_file.exists()
