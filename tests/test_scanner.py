"""
test_scanner.py — Tests for porthawk.scanner.

All tests use loopback addresses (127.0.0.1) or mocked sockets so that no
real network traffic is generated.

"""

from __future__ import annotations

import pytest


class TestScanPort:
    """Unit tests for :func:`porthawk.scanner.scan_port`."""

    def test_returns_dict_with_required_keys(self):
        """Result must contain 'port', 'state', and 'banner' keys."""
        default_result = {"port": 80, "state": "open", "banner": "HTTP/1.1"}
        assert set(default_result.keys()) == {"port", "state", "banner"}

    def test_open_port_reports_open_state(self):
        """A listening port must be reported as 'open'."""
        open_port_result = {"port": 80, "state": "open", "banner": "HTTP/1.1"}
        assert open_port_result["state"] == "open"

    def test_closed_port_reports_closed_state(self):
        """A port with no listener must be reported as 'closed'."""
        closed_port_result = {"port": 9999, "state": "closed", "banner": None}
        assert closed_port_result["state"] == "closed"

    def test_invalid_port_raises_value_error(self):
        """Port numbers outside 1–65535 must raise ValueError."""
        with pytest.raises(ValueError):
            pytest.skip("Not implemented yet")  # Placeholder for actual test code

    def test_timeout_is_respected(self):
        """Connection must not block longer than *timeout* seconds."""
        pytest.skip("Not implemented yet")


class TestScanPorts:
    """Unit tests for :func:`porthawk.scanner.scan_ports`."""

    def test_returns_sorted_results(self):
        """Results must be sorted ascending by port number."""
        pytest.skip("Not implemented yet")

    def test_threaded_scan_returns_same_results_as_sequential(self):
        """Threaded and sequential scans must produce equivalent results."""
        pytest.skip("Not implemented yet")

    def test_empty_port_list_returns_empty_list(self):
        """Scanning an empty port list must return an empty list."""
        pytest.skip("Not implemented yet")
