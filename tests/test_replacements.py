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

    def test_non_ascii_case_insensitive(self) -> None:
        """Regression: non-ASCII replacements must be case-insensitive when lowercase=True."""
        assert slugify("CAFÉ", replacements={"café": "coffee"}) == "coffee"
        assert slugify("Café", replacements={"café": "coffee"}) == "coffee"
        assert slugify("café", replacements={"café": "coffee"}) == "coffee"

    def test_non_ascii_case_sensitive_when_no_lowercase(self) -> None:
        """When lowercase=False, non-ASCII replacements are case-sensitive."""
        assert slugify("café", replacements={"café": "coffee"}, lowercase=False) == "coffee"
        assert slugify("CAFÉ", replacements={"café": "coffee"}, lowercase=False) == "CAFE"

    def test_post_replacement_value_lowercased(self) -> None:
        """Regression: post-replacement values must be lowercased when lowercase=True."""
        assert slugify("hello", replacements={"hello": "FOO"}) == "foo"
        assert slugify("hello", replacements={"hello": "FooBar"}) == "foobar"

    def test_post_replacement_value_preserved_when_no_lowercase(self) -> None:
        """When lowercase=False, post-replacement values preserve case."""
        assert slugify("hello", replacements={"hello": "FOO"}, lowercase=False) == "FOO"

    def test_non_ascii_replacement_with_backslash(self) -> None:
        """Regression: replacement values with backslash sequences must not crash."""
        assert slugify("café", replacements={"café": r"hello\1world"}) == "hello-1world"
        assert slugify("CAFÉ", replacements={"café": r"hello\1world"}) == "hello-1world"

    def test_post_replacement_case_insensitive_when_lowercase(self) -> None:
        """Regression: ASCII post-replacements must be case-insensitive when lowercase=True."""
        assert slugify("HELLO", replacements=[("H", "WORLD")], lowercase=True) == "worldello"
        assert slugify("hello", replacements=[("H", "WORLD")], lowercase=True) == "worldello"
        assert slugify("Hello", replacements=[("H", "WORLD")], lowercase=True) == "worldello"
