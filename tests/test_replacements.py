from __future__ import annotations

from slugany import slugify


class TestReplacements:
    def test_pre_replacement(self) -> None:
        assert slugify("café", replacements=[("é", "e")]) == "cafe"

    def test_post_replacement(self) -> None:
        assert slugify("hello world", replacements=[("world", "earth")]) == "hello-earth"

    def test_no_replacements(self) -> None:
        assert slugify("hello world") == "hello-world"

    def test_no_match(self) -> None:
        assert slugify("hello world", replacements=[("xyz", "abc")]) == "hello-world"

    def test_multiple(self) -> None:
        assert (
            slugify("foo bar baz", replacements=[("foo", "qux"), ("baz", "quux")]) == "qux-bar-quux"
        )

    def test_with_unicode(self) -> None:
        assert slugify("España", replacements=[("ñ", "ny")]) == "espanya"
