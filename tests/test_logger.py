"""
test_logger.py — Tests for porthawk.logger.

TODO: Replace each ``pytest.skip`` call with a real test implementation once
      the corresponding production code is written.
"""

from __future__ import annotations

import logging
from pathlib import Path

import pytest

from porthawk.logger import get_logger


class TestGetLogger:
    """Unit tests for :func:`porthawk.logger.get_logger`."""

    def test_returns_logger_instance(self):
        """Return value must be a logging.Logger."""
        returned_logger = get_logger("porthawk.test.returns")
        assert isinstance(returned_logger, logging.Logger)

    def test_default_level_is_info(self):
        """Logger effective level must be INFO when no level is specified."""
        logger = get_logger("porthawk.test.default_level")
        assert logger.getEffectiveLevel() == logging.INFO

    def test_custom_level_is_applied(self):
        """Logger must honour a custom level (e.g. DEBUG)."""
        logger = get_logger("porthawk.test.custom_level", level=logging.DEBUG)
        assert logger.getEffectiveLevel() == logging.DEBUG

    def test_no_duplicate_handlers_on_repeated_calls(self):
        """Calling get_logger twice with the same name must not add duplicate
        handlers."""
        logger_name = "porthawk.test.no_duplicates"
        first_logger = get_logger(logger_name)
        initial_handler_count = len(first_logger.handlers)

        second_logger = get_logger(logger_name)
        assert len(second_logger.handlers) == initial_handler_count

    def test_file_handler_created_when_log_file_given(self, tmp_path: Path):
        """A FileHandler must be attached when *log_file* is supplied."""
        log_file = tmp_path / "porthawk.log"
        logger = get_logger("porthawk.test.file_handler", log_file=log_file)

        file_handlers = [
            handler for handler in logger.handlers if isinstance(handler, logging.FileHandler)
        ]
        assert len(file_handlers) == 1
        assert Path(file_handlers[0].baseFilename) == log_file.resolve()
