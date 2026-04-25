"""
porthawk/__main__.py — Command-line entry point for PortHawk.

Enables both:
    python -m porthawk <args>
    porthawk <args>           (after pip install)

Usage (once implemented)
------------------------
    python -m porthawk <host> [--ports <range>] [--timeout <seconds>]
                              [--threads] [--output-json <file>]
                              [--output-csv <file>] [--log-file <file>]
                              [--verbose]

    # Examples:
    python -m porthawk 127.0.0.1 --ports 1-1024
    python -m porthawk 192.168.1.1 --ports 22,80,443 --threads --output-json results.json

IMPORTANT: Only scan hosts you own or have explicit written permission to test.

TODO: Implement argument parsing (argparse) and wire together the modules in
      porthawk/scanner.py, porthawk/output.py, and porthawk/logger.py.
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .logger import get_logger
from .output import write_csv, write_json
from .scanner import scan_ports


def _parse_port_token(token: str) -> list[int]:
    """Parse one port token (single value or range) into a list of ports."""
    token = token.strip()
    if not token:
        return []

    if "-" in token:
        start_raw, end_raw = token.split("-", 1)
        try:
            start = int(start_raw.strip())
            end = int(end_raw.strip())
        except ValueError as exc:
            raise ValueError(f"Invalid port range: {token}") from exc

        if start > end:
            raise ValueError(f"Invalid port range (start > end): {token}")
        if start < 1 or end > 65535:
            raise ValueError(f"Port range out of bounds (1-65535): {token}")
        return list(range(start, end + 1))

    try:
        port = int(token)
    except ValueError as exc:
        raise ValueError(f"Invalid port value: {token}") from exc

    if port < 1 or port > 65535:
        raise ValueError(f"Port out of bounds (1-65535): {token}")
    return [port]


def parse_ports(spec: str) -> list[int]:
    """Parse a ports specification like '22,80,443' or '1-1024,8080'."""
    ports: set[int] = set()
    for token in spec.split(","):
        ports.update(_parse_port_token(token))

    if not ports:
        raise ValueError("No ports were provided.")

    return sorted(ports)


def build_parser() -> argparse.ArgumentParser:
    """Build and return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="porthawk",
        description=(
            "Educational TCP port scanner. Scan only systems you own or have explicit permission to test."
        ),
    )

    parser.add_argument("host", help="Target hostname or IP address.")
    parser.add_argument(
        "--ports",
        default="1-1024",
        help="Comma-separated ports and/or ranges (e.g. 22,80,443 or 1-1024).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Per-port timeout in seconds (default: 1.0).",
    )
    parser.add_argument(
        "--threads",
        action="store_true",
        help="Enable threaded scanning.",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=100,
        help="Maximum worker threads when --threads is enabled (default: 100).",
    )
    parser.add_argument(
        "--output-json",
        type=Path,
        help="Write results to a JSON file.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        help="Write results to a CSV file.",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        help="Optional log file path.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug logging.",
    )
    parser.add_argument(
        "--show-all",
        action="store_true",
        help="Print a detailed table for all scanned ports.",
    )

    return parser


def _print_table(results: list[dict]) -> None:
    """Print all scan results in a compact fixed-width table."""
    port_width = max(len("PORT"), max((len(str(r["port"])) for r in results), default=4))
    state_width = max(len("STATE"), max((len(str(r["state"])) for r in results), default=5))

    header = f"{'PORT':<{port_width}}  {'STATE':<{state_width}}  BANNER"
    separator = f"{'-' * port_width}  {'-' * state_width}  {'-' * 6}"
    print(header)
    print(separator)

    for result in results:
        banner = result.get("banner") or "-"
        print(f"{result['port']:<{port_width}}  {result['state']:<{state_width}}  {banner}")


def _print_summary(host: str, results: list[dict], show_all: bool = False) -> None:
    """Print a compact text summary to stdout."""
    open_ports = [r for r in results if r["state"] == "open"]
    print(f"Scanned {len(results)} ports on {host}.")
    print(f"Open ports: {len(open_ports)}")

    if show_all:
        _print_table(results)
        return

    for result in open_ports:
        banner = result.get("banner")
        banner_text = f" - {banner}" if banner else ""
        print(f"  {result['port']}/tcp open{banner_text}")


def main() -> None:
    """Parse CLI arguments and run the port scanner."""
    parser = build_parser()
    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    log = get_logger(name="porthawk", level=log_level, log_file=args.log_file)

    try:
        ports = parse_ports(args.ports)
    except ValueError as exc:
        parser.error(str(exc))

    log.info("Starting scan host=%s ports=%d threaded=%s", args.host, len(ports), args.threads)

    try:
        results = scan_ports(
            host=args.host,
            ports=ports,
            timeout=args.timeout,
            use_threads=args.threads,
            max_workers=args.max_workers,
        )
    except ValueError as exc:
        parser.error(str(exc))
    except Exception as exc:
        log.error("Scan failed: %s", exc)
        raise SystemExit(1) from exc

    _print_summary(args.host, results, show_all=args.show_all)

    if args.output_json is not None:
        write_json(results, args.output_json)
        log.info("Wrote JSON output to %s", args.output_json)

    if args.output_csv is not None:
        write_csv(results, args.output_csv)
        log.info("Wrote CSV output to %s", args.output_csv)

    log.info("Scan finished.")


if __name__ == "__main__":
    main()
