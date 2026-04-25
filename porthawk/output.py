"""
output.py — Serialise scan results to JSON and CSV.

Responsibilities
----------------
- Accept the list of result dicts produced by :mod:`porthawk.scanner`.
- Write results to a JSON file (pretty-printed, UTF-8).
- Write results to a CSV file with a header row.
- Both writers should create parent directories if they don't exist.

Expected result dict schema (at minimum):
    {
        "port": int,
        "state": "open" | "closed" | "filtered",
        "banner": str | None,
    }

"""

from __future__ import annotations

import csv
import json
from pathlib import Path


def write_json(results: list[dict], filepath: str | Path) -> None:
    """Serialise *results* to a pretty-printed JSON file at *filepath*.

    Parameters
    ----------
    results:
        List of port-scan result dicts.
    filepath:
        Destination file path.  Parent directories are created automatically.
    """
    if not results:
        raise ValueError("Results list cannot be empty.")
    if isinstance(filepath, str):
        filepath = Path(filepath)
    if not filepath.parent.exists():
        filepath.parent.mkdir(parents=True, exist_ok=True)
    with filepath.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)


def write_csv(results: list[dict], filepath: str | Path) -> None:
    """Serialise *results* to a CSV file at *filepath*.

    The first row must be a header derived from the dict keys.

    Parameters
    ----------
    results:
        List of port-scan result dicts.  Must be non-empty so that the
        column headers can be inferred.
    filepath:
        Destination file path.  Parent directories are created automatically.

    Raises
    ------
    ValueError
        If *results* is empty.
    """
    if not results:
        raise ValueError("Results list cannot be empty.")
    if isinstance(filepath, str):
        filepath = Path(filepath)
    if not filepath.parent.exists():
        filepath.parent.mkdir(parents=True, exist_ok=True)
    with filepath.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

