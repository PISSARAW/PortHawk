"""test_main.py — Tests for porthawk.__main__ CLI helpers and entry flow."""

from __future__ import annotations

import pytest

from porthawk import __main__ as cli


class TestParsePorts:
    """Unit tests for :func:`porthawk.__main__.parse_ports`."""

    def test_parses_single_ports_and_ranges(self):
        assert cli.parse_ports("22,80,443") == [22, 80, 443]
        assert cli.parse_ports("1-3,10") == [1, 2, 3, 10]

    def test_deduplicates_and_sorts_ports(self):
        assert cli.parse_ports("80,22,80,21-23") == [21, 22, 23, 80]

    def test_raises_on_invalid_value(self):
        with pytest.raises(ValueError):
            cli.parse_ports("abc")

    def test_raises_on_out_of_range(self):
        with pytest.raises(ValueError):
            cli.parse_ports("0,65536")

    def test_raises_on_reversed_range(self):
        with pytest.raises(ValueError):
            cli.parse_ports("100-10")


class TestSummaryOutput:
    """Unit tests for summary and table printing helpers."""

    def test_summary_prints_only_open_ports_by_default(self, capsys: pytest.CaptureFixture[str]):
        results = [
            {"port": 22, "state": "open", "banner": "SSH"},
            {"port": 80, "state": "closed", "banner": None},
        ]

        cli._print_summary("127.0.0.1", results, show_all=False)
        out = capsys.readouterr().out

        assert "Scanned 2 ports on 127.0.0.1." in out
        assert "Open ports: 1" in out
        assert "22/tcp open - SSH" in out
        assert "80/tcp" not in out

    def test_summary_prints_table_when_show_all(self, capsys: pytest.CaptureFixture[str]):
        results = [
            {"port": 22, "state": "open", "banner": "SSH"},
            {"port": 443, "state": "closed", "banner": None},
        ]

        cli._print_summary("127.0.0.1", results, show_all=True)
        out = capsys.readouterr().out

        assert "PORT" in out and "STATE" in out and "BANNER" in out
        assert "22" in out and "open" in out and "SSH" in out
        assert "443" in out and "closed" in out


class TestMain:
    """High-level tests for :func:`porthawk.__main__.main`."""

    def test_main_wires_scan_and_outputs(self, monkeypatch: pytest.MonkeyPatch):
        called: dict[str, object] = {}

        sample_results = [
            {"port": 22, "state": "open", "banner": "SSH"},
            {"port": 80, "state": "closed", "banner": None},
        ]

        class DummyLogger:
            def info(self, *args, **kwargs):
                return None

            def error(self, *args, **kwargs):
                return None

        def fake_get_logger(*args, **kwargs):
            return DummyLogger()

        def fake_scan_ports(host, ports, timeout, use_threads, max_workers):
            called["scan"] = {
                "host": host,
                "ports": ports,
                "timeout": timeout,
                "use_threads": use_threads,
                "max_workers": max_workers,
            }
            return sample_results

        def fake_write_json(results, path):
            called["json"] = {"results": results, "path": str(path)}

        def fake_write_csv(results, path):
            called["csv"] = {"results": results, "path": str(path)}

        def fake_print_summary(host, results, show_all=False):
            called["summary"] = {"host": host, "results": results, "show_all": show_all}

        monkeypatch.setattr(cli, "get_logger", fake_get_logger)
        monkeypatch.setattr(cli, "scan_ports", fake_scan_ports)
        monkeypatch.setattr(cli, "write_json", fake_write_json)
        monkeypatch.setattr(cli, "write_csv", fake_write_csv)
        monkeypatch.setattr(cli, "_print_summary", fake_print_summary)
        monkeypatch.setattr(
            "sys.argv",
            [
                "porthawk",
                "127.0.0.1",
                "--ports",
                "22,80",
                "--timeout",
                "2.5",
                "--threads",
                "--max-workers",
                "8",
                "--output-json",
                "results.json",
                "--output-csv",
                "results.csv",
                "--show-all",
            ],
        )

        cli.main()

        assert called["scan"] == {
            "host": "127.0.0.1",
            "ports": [22, 80],
            "timeout": 2.5,
            "use_threads": True,
            "max_workers": 8,
        }
        assert called["summary"] == {
            "host": "127.0.0.1",
            "results": sample_results,
            "show_all": True,
        }
        assert called["json"] == {"results": sample_results, "path": "results.json"}
        assert called["csv"] == {"results": sample_results, "path": "results.csv"}

    def test_main_exits_with_parser_error_on_bad_ports(self, monkeypatch: pytest.MonkeyPatch):
        monkeypatch.setattr("sys.argv", ["porthawk", "127.0.0.1", "--ports", "70000"])

        with pytest.raises(SystemExit) as exc:
            cli.main()

        assert exc.value.code == 2
