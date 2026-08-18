from __future__ import annotations

from slugany import is_slug


class TestIsSlug:
    def test_valid_slug(self) -> None:
        assert is_slug("hello-world") is True

    def test_single_word(self) -> None:
        assert is_slug("hello") is True

    def test_numbers(self) -> None:
        assert is_slug("hello123-world456") is True

    def test_only_numbers(self) -> None:
        assert is_slug("123-456") is True

    def test_invalid_space(self) -> None:
        assert is_slug("hello world") is False

    def test_invalid_double_sep(self) -> None:
        assert is_slug("hello--world") is False

    def test_invalid_leading(self) -> None:
        assert is_slug("-hello-world") is False

    def test_invalid_trailing(self) -> None:
        assert is_slug("hello-world-") is False

    def test_invalid_empty(self) -> None:
        assert is_slug("") is False

    def test_invalid_special_chars(self) -> None:
        assert is_slug("hello@world") is False

    def test_custom_separator_underscore(self) -> None:
        assert is_slug("hello_world", separator="_") is True

    def test_custom_separator_dot(self) -> None:
        assert is_slug("hello.world", separator=".") is True

    def test_custom_separator_double(self) -> None:
        assert is_slug("hello--world", separator="--") is True
