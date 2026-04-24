"""
test_logger.py — Tests for porthawk.logger.

TODO: Replace each ``pytest.skip`` call with a real test implementation once
      the corresponding production code is written.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pytest


class TestGetLogger:
    """Unit tests for :func:`porthawk.logger.get_logger`."""

    def test_returns_logger_instance(self):
        """Return value must be a logging.Logger."""
        pytest.skip("Not implemented yet")

    def test_default_level_is_info(self):
        """Logger effective level must be INFO when no level is specified."""
        pytest.skip("Not implemented yet")

    def test_custom_level_is_applied(self):
        """Logger must honour a custom level (e.g. DEBUG)."""
        pytest.skip("Not implemented yet")

    def test_no_duplicate_handlers_on_repeated_calls(self):
        """Calling get_logger twice with the same name must not add duplicate
        handlers."""
        pytest.skip("Not implemented yet")

    def test_file_handler_created_when_log_file_given(self, tmp_path: Path):
        """A FileHandler must be attached when *log_file* is supplied."""
        pytest.skip("Not implemented yet")
