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
    logger = logging.getLogger(name)

    resolved_log_file: Path | None = None
    if log_file is not None:
        resolved_log_file = Path(log_file).expanduser().resolve()
        if resolved_log_file.exists() and not resolved_log_file.is_file():
            raise ValueError(f"Log file path {resolved_log_file} is not a file.")
        resolved_log_file.parent.mkdir(parents=True, exist_ok=True)

    logger.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    existing_stream_handler = next(
        (
            handler
            for handler in logger.handlers
            if isinstance(handler, logging.StreamHandler)
            and not isinstance(handler, logging.FileHandler)
            and getattr(handler, "_porthawk_stream", False)
        ),
        None,
    )

    if existing_stream_handler is None:
        stream_handler = logging.StreamHandler()
        setattr(stream_handler, "_porthawk_stream", True)
        logger.addHandler(stream_handler)
        existing_stream_handler = stream_handler

    existing_stream_handler.setLevel(level)
    existing_stream_handler.setFormatter(formatter)

    if resolved_log_file is not None:
        existing_file_handler = next(
            (
                handler
                for handler in logger.handlers
                if isinstance(handler, logging.FileHandler)
                and Path(handler.baseFilename).resolve() == resolved_log_file
            ),
            None,
        )
        if existing_file_handler is None:
            file_handler = logging.FileHandler(resolved_log_file, mode="a")
            logger.addHandler(file_handler)
            existing_file_handler = file_handler

        existing_file_handler.setLevel(level)
        existing_file_handler.setFormatter(formatter)

    return logger