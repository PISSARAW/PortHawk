"""
scanner.py — Core TCP port scanning logic.

Responsibilities
----------------
- Connect to a target host/port using a raw socket (TCP connect scan).
- Support an optional connection timeout (seconds).
- Support optional multi-threading to scan multiple ports concurrently.
- Return a result dict for every port that includes at least:
    {
        "port": int,
        "state": "open" | "closed" | "filtered",
        "banner": str | None,
    }

"""

from __future__ import annotations

import socket
import threading
from typing import Iterable


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------


def scan_port(host: str, port: int, timeout: float = 1.0) -> dict:
    """Attempt a TCP connection to *host*:*port* and return a result dict.

    Parameters
    ----------
    host:
        Target hostname or IP address.
    port:
        TCP port number (1–65535).
    timeout:
        Socket connection timeout in seconds.

    Returns
    -------
    dict
        Keys: ``port`` (int), ``state`` (str), ``banner`` (str | None).

    Raises
    ------
    ValueError
        If *port* is outside the valid range 1–65535.
    """
    if not (1 <= port <= 65535):
        raise ValueError(f"Port number {port} is out of valid range (1–65535).")
    if timeout <= 0:
        raise ValueError("Timeout must be a positive number.")
    if not host:
        raise ValueError("Host cannot be empty.")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        try:
            banner = sock.recv(1024).decode(errors="ignore").strip() or None
        except socket.timeout:
            banner = None
        state = "open"
    except (socket.timeout, ConnectionRefusedError):
        state = "closed"
        banner = None
    except OSError:
        state = "filtered"
        banner = None
    finally:
        sock.close()
    return {"port": port, "state": state, "banner": banner}    
    


# ---------------------------------------------------------------------------
# Multi-port scanning
# ---------------------------------------------------------------------------


def scan_ports(
    host: str,
    ports: Iterable[int],
    timeout: float = 1.0,
    use_threads: bool = False,
    max_workers: int = 100,
) -> list[dict]:
    """Scan multiple *ports* on *host* and return a list of result dicts.

    Parameters
    ----------
    host:
        Target hostname or IP address.
    ports:
        An iterable of port numbers to scan.
    timeout:
        Per-port connection timeout in seconds.
    use_threads:
        When ``True``, ports are scanned concurrently using a thread pool.
    max_workers:
        Maximum number of concurrent threads (only used when
        ``use_threads=True``).

    Returns
    -------
    list[dict]
        One result dict per port (see :func:`scan_port` for the schema),
        sorted ascending by port number.
    """
    if not host:
        raise ValueError("Host cannot be empty.")
    if timeout <= 0:
        raise ValueError("Timeout must be a positive number.")
    if use_threads and max_workers <= 0:
        raise ValueError("max_workers must be a positive integer.")
    if use_threads:
        from concurrent.futures import ThreadPoolExecutor, as_completed

        results = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_port = {executor.submit(scan_port, host, port, timeout): port for port in ports}
            for future in as_completed(future_to_port):
                results.append(future.result())
        return sorted(results, key=lambda r: r["port"])
    else:
        return sorted((scan_port(host, port, timeout) for port in ports), key=lambda r: r["port"]) 
