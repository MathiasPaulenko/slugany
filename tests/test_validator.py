from __future__ import annotations

import pytest

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

    def test_unicode_slug_default(self) -> None:
        assert is_slug("espa\u00f1a") is False

    def test_unicode_slug_allowed(self) -> None:
        assert is_slug("espa\u00f1a", allow_unicode=True) is True

    def test_unicode_slug_with_separator(self) -> None:
        assert is_slug("espa\u00f1a-mundo", allow_unicode=True) is True

    def test_unicode_slug_invalid_chars(self) -> None:
        assert is_slug("espa\u00f1a mundo", allow_unicode=True) is False

    def test_unicode_slug_leading_sep(self) -> None:
        assert is_slug("-espa\u00f1a", allow_unicode=True) is False

    def test_non_string_input_raises(self) -> None:
        with pytest.raises(TypeError):
            is_slug(123)  # type: ignore[arg-type]

    def test_non_string_separator_raises(self) -> None:
        with pytest.raises(TypeError):
            is_slug("hello-world", separator=123)  # type: ignore[arg-type]

    def test_separator_underscore(self) -> None:
        assert is_slug("hello_world_foo", separator="_") is True
        assert is_slug("hello-world", separator="_") is False

    def test_separator_dot(self) -> None:
        assert is_slug("hello.world.foo", separator=".") is True
        assert is_slug("hello-world", separator=".") is False

    def test_separator_empty_string(self) -> None:
        assert is_slug("helloworld", separator="") is True
        assert is_slug("hello world", separator="") is False

    def test_separator_empty_no_redos(self) -> None:
        """Regression: empty separator must not cause catastrophic backtracking."""
        import time

        start = time.time()
        result = is_slug("a" * 100 + "!", separator="")
        elapsed = time.time() - start
        assert result is False
        assert elapsed < 1.0
