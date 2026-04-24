"""
test_banner.py — Tests for porthawk.banner.

TODO: Replace each ``pytest.skip`` call with a real test implementation once
      the corresponding production code is written.
"""

from __future__ import annotations

import pytest


class TestGrabBanner:
    """Unit tests for :func:`porthawk.banner.grab_banner`."""

    def test_returns_string_when_service_sends_data(self):
        """A service that sends data must return a non-empty string."""
        pytest.skip("Not implemented yet")

    def test_returns_none_when_service_is_silent(self):
        """A service that sends nothing must return None within timeout."""
        pytest.skip("Not implemented yet")

    def test_strips_whitespace_from_banner(self):
        """Leading and trailing whitespace must be stripped from the banner."""
        pytest.skip("Not implemented yet")

    def test_respects_max_bytes(self):
        """No more than *max_bytes* must be read from the socket."""
        pytest.skip("Not implemented yet")

    def test_timeout_does_not_block(self):
        """grab_banner must return within approximately *timeout* seconds."""
        pytest.skip("Not implemented yet")
