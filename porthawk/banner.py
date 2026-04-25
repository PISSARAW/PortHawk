"""
banner.py — Service banner grabbing over an existing TCP connection.

Responsibilities
----------------
- Receive the initial bytes sent by a service after a successful connection
  (the "banner") and decode them to a string.
- Honour a configurable read timeout to avoid hanging on silent services.
- Return ``None`` when no banner is available within the timeout.

"""

from __future__ import annotations

import socket


def grab_banner(
    host: str,
    port: int,
    timeout: float = 2.0,
    max_bytes: int = 1024,
) -> str | None:
    """Connect to *host*:*port*, read up to *max_bytes*, and return the banner.

    Parameters
    ----------
    host:
        Target hostname or IP address.
    port:
        TCP port number.
    timeout:
        Read timeout in seconds.  If the service does not send data within
        this window, ``None`` is returned.
    max_bytes:
        Maximum number of bytes to read from the socket.

    Returns
    -------
    str | None
        The decoded banner string, stripped of leading/trailing whitespace,
        or ``None`` if no banner was received.
    """
    raise NotImplementedError
