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


def main() -> None:
    """Parse CLI arguments and run the port scanner."""
    raise NotImplementedError


if __name__ == "__main__":
    main()
