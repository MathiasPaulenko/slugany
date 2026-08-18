from __future__ import annotations

from slugany import slugify


class TestSmartPunctuation:
    def test_curly_single_quotes(self) -> None:
        assert slugify("Bob\u2019s caf\u00e9") == "bob-s-cafe"

    def test_curly_double_quotes(self) -> None:
        assert slugify("\u201cHello\u201d World") == "hello-world"

    def test_em_dash(self) -> None:
        assert slugify("Hello\u2014World") == "hello-world"

    def test_en_dash(self) -> None:
        assert slugify("Hello\u2013World") == "hello-world"

    def test_nbsp(self) -> None:
        assert slugify("Hello\u00a0World") == "hello-world"

    def test_zero_width(self) -> None:
        assert slugify("Hello\u200bWorld") == "helloworld"

    def test_zero_width_joiner(self) -> None:
        assert slugify("Hello\u200dWorld") == "helloworld"

    def test_bullet(self) -> None:
        assert slugify("Hello\u2022World") == "hello-world"

    def test_disabled(self) -> None:
        assert slugify("Bob\u2019s caf\u00e9", smart_punctuation=False) == "bobs-cafe"
