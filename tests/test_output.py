"""
test_output.py — Tests for porthawk.output.

TODO: Replace each ``pytest.skip`` call with a real test implementation once
      the corresponding production code is written.
"""

from __future__ import annotations

import json
import csv
from pathlib import Path

import pytest


SAMPLE_RESULTS = [
    {"port": 22, "state": "open", "banner": "SSH-2.0-OpenSSH_9.0"},
    {"port": 80, "state": "open", "banner": None},
    {"port": 443, "state": "closed", "banner": None},
]


class TestWriteJson:
    """Unit tests for :func:`porthawk.output.write_json`."""

    def test_creates_valid_json_file(self, tmp_path: Path):
        """Output must be a valid JSON file containing all results."""
        pytest.skip("Not implemented yet")

    def test_creates_parent_directories(self, tmp_path: Path):
        """Parent directories must be created if they do not exist."""
        pytest.skip("Not implemented yet")

    def test_json_is_pretty_printed(self, tmp_path: Path):
        """JSON must be indented (pretty-printed), not minified."""
        pytest.skip("Not implemented yet")


class TestWriteCsv:
    """Unit tests for :func:`porthawk.output.write_csv`."""

    def test_creates_csv_with_header(self, tmp_path: Path):
        """Output must be a CSV file with a header row."""
        pytest.skip("Not implemented yet")

    def test_csv_row_count_matches_results(self, tmp_path: Path):
        """CSV must have exactly len(results) data rows (excluding header)."""
        pytest.skip("Not implemented yet")

    def test_raises_on_empty_results(self, tmp_path: Path):
        """Passing an empty list must raise ValueError."""
        pytest.skip("Not implemented yet")

    def test_creates_parent_directories(self, tmp_path: Path):
        """Parent directories must be created if they do not exist."""
        pytest.skip("Not implemented yet")
