"""
logger.py — Centralised logging configuration for PortHawk.

Responsibilities
----------------
- Create and return a :class:`logging.Logger` configured with:
    * A ``StreamHandler`` that writes to *stderr* at the requested level.
    * An optional ``FileHandler`` that appends to a log file.
- Use a consistent, human-readable format that includes timestamp, level,
  and message.
- Ensure calling ``get_logger`` multiple times with the same name does not
  add duplicate handlers.

TODO: Implement the following stub.
"""

from __future__ import annotations

import logging
from pathlib import Path


def get_logger(
    name: str = "porthawk",
    level: int = logging.INFO,
    log_file: str | Path | None = None,
) -> logging.Logger:
    """Return a configured :class:`logging.Logger`.

    Parameters
    ----------
    name:
        Logger name (typically ``__name__`` of the calling module).
    level:
        Minimum log level (e.g. ``logging.DEBUG``, ``logging.INFO``).
    log_file:
        Optional path to a log file.  When supplied, log records are also
        written to that file in addition to *stderr*.

    Returns
    -------
    logging.Logger
        A ready-to-use logger instance.
    """
    raise NotImplementedError
