"""
test_output.py — Tests for porthawk.output.


"""

from __future__ import annotations

import json
import csv
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
        if isinstance(tmp_path, str):
            tmp_path = Path(tmp_path)
        json_file = tmp_path / "results.json"
        write_json(SAMPLE_RESULTS, json_file)  
        assert json_file.exists()
        with json_file.open("r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        assert loaded_data == SAMPLE_RESULTS

    def test_creates_parent_directories(self, tmp_path: Path):
        """Parent directories must be created if they do not exist."""
        if isinstance(tmp_path, str):
            tmp_path = Path(tmp_path)
        json_file = tmp_path / "results.json"
        write_json(SAMPLE_RESULTS, json_file)  
        assert json_file.exists()

    def test_json_is_pretty_printed(self, tmp_path: Path):
        """JSON must be indented (pretty-printed), not minified."""
        if isinstance(tmp_path, str):
            tmp_path = Path(tmp_path)
        json_file = tmp_path / "results.json"
        write_json(SAMPLE_RESULTS, json_file)  
        with json_file.open("r", encoding="utf-8") as f:
            content = f.read()
        assert "\n" in content and "    " in content  # Check for newlines and indentation


class TestWriteCsv:
    """Unit tests for :func:`porthawk.output.write_csv`."""

    def test_creates_csv_with_header(self, tmp_path: Path):
        """Output must be a CSV file with a header row."""
        if isinstance(tmp_path, str):
            tmp_path = Path(tmp_path)
        csv_file = tmp_path / "results.csv"
        write_csv(SAMPLE_RESULTS, csv_file)
        assert csv_file.exists()
        with csv_file.open("r", encoding="utf-8") as f:
            reader = csv.reader(f)
            header = next(reader)
            assert header == ["port", "state", "banner"]

    def test_csv_row_count_matches_results(self, tmp_path: Path):
        """CSV must have exactly len(results) data rows (excluding header)."""
        if isinstance(tmp_path, str):
            tmp_path = Path(tmp_path)
        csv_file = tmp_path / "results.csv"
        write_csv(SAMPLE_RESULTS, csv_file)
        with csv_file.open("r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            rows = list(reader)
        assert len(rows) == len(SAMPLE_RESULTS)

    def test_raises_on_empty_results(self, tmp_path: Path):
        """Passing an empty list must raise ValueError."""
        if isinstance(tmp_path, str):
            tmp_path = Path(tmp_path)
        csv_file = tmp_path / "results.csv"
        with pytest.raises(ValueError):
            write_csv([], csv_file)

    def test_creates_parent_directories(self, tmp_path: Path):
        """Parent directories must be created if they do not exist."""
        if isinstance(tmp_path, str):
            tmp_path = Path(tmp_path)
        csv_file = tmp_path / "results.csv"
        write_csv(SAMPLE_RESULTS, csv_file)
        assert csv_file.exists()
