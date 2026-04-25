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
    if log_file is not None:
        log_file = Path(log_file)   
    if log_file is not None and not log_file.parent.exists():
        log_file.parent.mkdir(parents=True, exist_ok=True)
    if log_file is not None and not log_file.exists():
        log_file.touch(exist_ok=True)
    if log_file is not None and not log_file.is_file():
        raise ValueError(f"Log file path {log_file} is not a file.")
    if log_file is not None and not log_file.is_absolute():
        log_file = log_file.resolve()
    else:
        logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    if not logger.hasHandlers():
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    if log_file is not None:
        file_handler = logging.FileHandler(log_file, mode="a")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    return logger