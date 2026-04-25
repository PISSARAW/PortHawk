"""Integration tests for running PortHawk through its CLI entry point."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_cli_module_runs_successfully_on_localhost():
    """`python -m porthawk` should run end-to-end and print a scan summary."""
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "porthawk",
            "127.0.0.1",
            "--ports",
            "1-3",
            "--timeout",
            "0.1",
            "--show-all",
        ],
        cwd=_project_root(),
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Scanned 3 ports on 127.0.0.1." in result.stdout
    assert "Open ports:" in result.stdout
    assert "PORT" in result.stdout and "STATE" in result.stdout and "BANNER" in result.stdout
