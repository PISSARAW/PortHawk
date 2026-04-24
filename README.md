# PortHawk

> **⚠️ ETHICAL USAGE DISCLAIMER**
>
> PortHawk is an **educational tool** intended solely for learning about
> network programming and security concepts.
>
> **You must only scan hosts that you own or have received explicit,
> written permission to test.**
>
> Unauthorised port scanning may violate the Computer Fraud and Abuse Act
> (CFAA), the Computer Misuse Act, or equivalent legislation in your
> jurisdiction. The authors accept **no liability** for misuse of this software.
> Use responsibly and legally.

---

## Overview

PortHawk is a lightweight TCP port scanner written in Python using the
standard library only. It is designed as a learning project to explore:

- Raw socket programming (`socket` module)
- Optional concurrent scanning with threads (`threading` / `concurrent.futures`)
- Connection timeout handling
- Service banner grabbing
- Structured output (JSON & CSV)
- Structured logging

## Project Structure

```
PortHawk/
├── porthawk/
│   ├── __init__.py
│   ├── __main__.py       # CLI entry point (python -m porthawk)
│   ├── scanner.py        # TCP connect scan + threading
│   ├── banner.py         # Banner grabbing
│   ├── output.py         # JSON / CSV serialisation
│   └── logger.py         # Logging configuration
├── tests/
│   ├── test_scanner.py
│   ├── test_banner.py
│   ├── test_output.py
│   └── test_logger.py
├── requirements.txt
├── pyproject.toml
├── LICENSE
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.10 or newer (standard library only — no third-party runtime deps)

### Installation

```bash
git clone https://github.com/PISSARAW/PortHawk.git
cd PortHawk
python -m venv .venv && source .venv/bin/activate  # optional but recommended
pip install -e ".[dev]"
```

### Running

```bash
# Once implemented:
python -m porthawk <host> [--ports <range>] [--threads] [--output-json out.json]
```

### Running Tests

```bash
pytest --tb=short
```

## Planned Features

- [x] Project skeleton & test stubs
- [ ] `scan_port()` — single TCP connect scan with timeout
- [ ] `scan_ports()` — multi-port scan (sequential & threaded)
- [ ] `grab_banner()` — read service banner after connect
- [ ] `write_json()` / `write_csv()` — structured output
- [ ] `get_logger()` — configurable logging to stderr and/or file
- [ ] `main()` — argparse CLI wiring everything together

## License

This project is licensed under the [MIT License](LICENSE).
