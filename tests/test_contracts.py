from __future__ import annotations

import random
import string

import pytest

from slugany import slugify


class TestIdempotency:
    def test_idempotency_basic(self) -> None:
        result = slugify("Hello World!")
        assert slugify(result) == result

    def test_idempotency_random(self) -> None:
        rng = random.Random(42)
        chars = (
            string.ascii_letters
            + string.digits
            + " \u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00fc\u00e7\u00df"
            + "\u2014\u2019\u201c\u201d\u00a1\u00bf\u00a0\u200b\U0001f600"
        )
        for _ in range(500):
            length = rng.randint(1, 50)
            text = "".join(rng.choice(chars) for _ in range(length))
            result = slugify(text)
            assert slugify(result) == result, f"Not idempotent for input {text!r} -> {result!r}"


class TestDeterminism:
    def test_determinism(self) -> None:
        text = "Caf\u00e9 r\u00e9sum\u00e9 \u00a1Hola Mundo!"
        first = slugify(text)
        for _ in range(100):
            assert slugify(text) == first


class TestAsciiOutput:
    def test_ascii_output(self) -> None:
        rng = random.Random(99)
        chars = (
            string.ascii_letters
            + string.digits
            + " \u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00fc\u00e7\u00df"
            + "\u2014\u2019\u201c\u201d\u00a1\u00bf\u00a0\u200b\U0001f600"
            + "\u0441\u0430\u0444\u0435"
        )
        for _ in range(200):
            length = rng.randint(1, 50)
            text = "".join(rng.choice(chars) for _ in range(length))
            result = slugify(text, allow_unicode=False)
            assert result.isascii(), f"Non-ASCII output for input {text!r} -> {result!r}"


class TestNoDoubleSeparator:
    def test_no_double_sep(self) -> None:
        rng = random.Random(77)
        chars = (
            string.ascii_letters
            + string.digits
            + " \u00e1\u00e9\u00ed\u00f3\u00fa\u00f1\u00fc\u00e7\u00df"
            + "\u2014\u2019\u201c\u201d\u00a1\u00bf\u00a0\u200b\U0001f600"
            + "\u0441\u0430\u0444\u0435"
        )
        for _ in range(300):
            length = rng.randint(1, 50)
            text = "".join(rng.choice(chars) for _ in range(length))
            result = slugify(text)
            assert "--" not in result, f"Double separator in {result!r} for input {text!r}"
            assert not result.startswith("-"), f"Leading separator in {result!r} for input {text!r}"
            assert not result.endswith("-"), f"Trailing separator in {result!r} for input {text!r}"


class TestNoEmptyCrash:
    def test_empty(self) -> None:
        assert slugify("") == ""

    def test_whitespace(self) -> None:
        assert slugify("   ") == ""

    def test_punctuation(self) -> None:
        assert slugify("!!!") == ""

    def test_emoji(self) -> None:
        assert slugify("\U0001f600\U0001f389") == ""

    def test_html_entities(self) -> None:
        assert slugify("&amp;") == ""

    def test_none_type_error(self) -> None:
        with pytest.raises(TypeError):
            slugify(None)  # type: ignore[arg-type]


class TestFallback:
    def test_empty(self) -> None:
        assert slugify("", fallback="untitled") == "untitled"

    def test_only_punctuation(self) -> None:
        assert slugify("!!!", fallback="untitled") == "untitled"

    def test_only_emoji(self) -> None:
        assert slugify("\U0001f600\U0001f389", fallback="untitled") == "untitled"

    def test_not_triggered(self) -> None:
        assert slugify("Hello World", fallback="untitled") == "hello-world"

    def test_empty_fallback(self) -> None:
        assert slugify("!!!", fallback="") == ""

    def test_no_fallback(self) -> None:
        assert slugify("!!!") == ""
