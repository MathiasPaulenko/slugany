from __future__ import annotations

import subprocess
import sys
from io import StringIO
from unittest.mock import patch

import pytest

from slugany.cli import _build_kwargs, _build_parser, main


class _ReconfigurableStringIO(StringIO):
    def reconfigure(self, encoding: str) -> None:
        pass


def _run_cli(args: list[str], stdin: str | None = None) -> str:
    result = subprocess.run(
        [sys.executable, "-m", "slugany.cli", *args],
        input=stdin,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    return result.stdout.strip()


class TestCLI:
    def test_basic(self) -> None:
        assert _run_cli(["Hello World"]) == "hello-world"

    def test_separator(self) -> None:
        assert _run_cli(["Hello World", "-s", "_"]) == "hello_world"

    def test_style(self) -> None:
        assert _run_cli(["hello world", "--style", "camel"]) == "helloWorld"

    def test_max_length(self) -> None:
        assert _run_cli(["hello-world-foo", "--max-length", "10"]) == "hello-worl"

    def test_stdin(self) -> None:
        assert _run_cli([], stdin="Caf\u00e9\n") == "cafe"

    def test_batch(self) -> None:
        output = _run_cli(["--batch"], stdin="Hello World\nCaf\u00e9\n")
        assert output == "hello-world\ncafe"

    def test_no_lowercase(self) -> None:
        assert _run_cli(["Hello World", "--no-lowercase"]) == "Hello-World"

    def test_lang(self) -> None:
        assert _run_cli(["\u00dcbung", "--lang", "de"]) == "uebung"

    def test_fallback(self) -> None:
        assert _run_cli(["!!!", "--fallback", "untitled"]) == "untitled"


class TestCLIDirect:
    def test_main_with_text(self) -> None:
        with patch("sys.stdout", new=StringIO()) as out:
            assert main(["Hello World"]) == 0
        assert out.getvalue().strip() == "hello-world"

    def test_main_with_separator(self) -> None:
        with patch("sys.stdout", new=StringIO()) as out:
            assert main(["Hello World", "-s", "_"]) == 0
        assert out.getvalue().strip() == "hello_world"

    def test_main_with_style(self) -> None:
        with patch("sys.stdout", new=StringIO()) as out:
            assert main(["hello world", "--style", "camel"]) == 0
        assert out.getvalue().strip() == "helloWorld"

    def test_main_with_max_length(self) -> None:
        with patch("sys.stdout", new=StringIO()) as out:
            assert main(["hello-world-foo", "--max-length", "10"]) == 0
        assert out.getvalue().strip() == "hello-worl"

    def test_main_with_word_boundary(self) -> None:
        with patch("sys.stdout", new=StringIO()) as out:
            assert main(["hello-world-foo", "--max-length", "10", "--word-boundary"]) == 0
        assert out.getvalue().strip() == "hello"

    def test_main_no_lowercase(self) -> None:
        with patch("sys.stdout", new=StringIO()) as out:
            assert main(["Hello World", "--no-lowercase"]) == 0
        assert out.getvalue().strip() == "Hello-World"

    def test_main_allow_unicode(self) -> None:
        with patch("sys.stdout", new=StringIO()) as out:
            assert main(["Espa\u00f1a", "--allow-unicode"]) == 0
        assert out.getvalue().strip() == "espa\u00f1a"

    def test_main_fallback(self) -> None:
        with patch("sys.stdout", new=StringIO()) as out:
            assert main(["!!!", "--fallback", "untitled"]) == 0
        assert out.getvalue().strip() == "untitled"

    def test_main_emoji_mode(self) -> None:
        with patch("sys.stdout", new=StringIO()) as out:
            assert main(["Hello \U0001f389", "--emoji-mode", "strip"]) == 0
        assert out.getvalue().strip() == "hello"

    def test_main_css_safe(self) -> None:
        with patch("sys.stdout", new=StringIO()) as out:
            assert main(["123 hello", "--css-safe"]) == 0
        assert out.getvalue().strip() == "s-123-hello"

    def test_main_lang(self) -> None:
        with patch("sys.stdout", new=StringIO()) as out:
            assert main(["\u00dcbung", "--lang", "de"]) == 0
        assert out.getvalue().strip() == "uebung"

    def test_main_stdin(self) -> None:
        with (
            patch("sys.stdin", new=StringIO("Caf\u00e9\n")),
            patch("sys.stdout", new=StringIO()) as out,
        ):
            assert main([]) == 0
        assert out.getvalue().strip() == "cafe"

    def test_main_batch(self) -> None:
        with (
            patch("sys.stdin", new=StringIO("Hello World\nCaf\u00e9\n")),
            patch("sys.stdout", new=StringIO()) as out,
        ):
            assert main(["--batch"]) == 0
        assert out.getvalue().strip() == "hello-world\ncafe"

    def test_main_utf8_reconfigure(self) -> None:
        """Reconfigure path is exercised when streams expose that method."""
        with (
            patch("sys.stdin", new=_ReconfigurableStringIO("Caf\u00e9\n")),
            patch("sys.stdout", new=_ReconfigurableStringIO()) as out,
        ):
            assert main([]) == 0
        assert out.getvalue().strip() == "cafe"

    def test_main_no_args_no_stdin(self) -> None:
        with (
            patch("sys.stdin", new=StringIO("")),
            patch("sys.stdin.isatty", return_value=True),
            patch("sys.stdout", new=StringIO()) as out,
        ):
            assert main([]) == 0
        assert "usage" in out.getvalue().lower()

    def test_main_invalid_style_returns_error(self) -> None:
        """Regression: CLI should show clean error for invalid style, not traceback."""
        with (
            patch("sys.stderr", new=StringIO()) as err,
            patch("sys.stdout", new=StringIO()),
        ):
            assert main(["hello", "--style", "invalid"]) == 1
        assert "error:" in err.getvalue()
        assert "Invalid style" in err.getvalue()

    def test_main_invalid_lang_returns_error(self) -> None:
        """Regression: CLI should show clean error for invalid lang."""
        with (
            patch("sys.stderr", new=StringIO()) as err,
            patch("sys.stdout", new=StringIO()),
        ):
            assert main(["hello", "--lang", "xx"]) == 1
        assert "error:" in err.getvalue()

    def test_main_invalid_emoji_mode_returns_error(self) -> None:
        """Regression: CLI argparse rejects invalid emoji_mode with exit code 2."""
        with pytest.raises(SystemExit) as exc_info:
            main(["hello", "--emoji-mode", "invalid"])
        assert exc_info.value.code == 2

    def test_main_stdin_isatty_false_empty(self) -> None:
        with (
            patch("sys.stdin", new=StringIO("")),
            patch("sys.stdin.isatty", return_value=False),
            patch("sys.stdout", new=StringIO()) as out,
        ):
            assert main([]) == 0
        assert out.getvalue() == ""

    def test_build_parser(self) -> None:
        parser = _build_parser()
        assert parser.prog == "slugany"

    def test_build_kwargs_empty(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(["Hello"])
        assert _build_kwargs(args) == {}

    def test_build_kwargs_all(self) -> None:
        parser = _build_parser()
        args = parser.parse_args(
            [
                "Hello",
                "-s",
                "_",
                "--style",
                "snake",
                "--lang",
                "es",
                "--max-length",
                "5",
                "--word-boundary",
                "--no-lowercase",
                "--allow-unicode",
                "--fallback",
                "x",
                "--emoji-mode",
                "keep",
                "--css-safe",
            ]
        )
        kwargs = _build_kwargs(args)
        assert kwargs["separator"] == "_"
        assert kwargs["style"] == "snake"
        assert kwargs["lang"] == "es"
        assert kwargs["max_length"] == 5
        assert kwargs["word_boundary"] is True
        assert kwargs["lowercase"] is False
        assert kwargs["allow_unicode"] is True
        assert kwargs["fallback"] == "x"
        assert kwargs["emoji_mode"] == "keep"
        assert kwargs["css_safe"] is True
