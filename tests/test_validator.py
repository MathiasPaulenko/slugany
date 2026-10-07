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

    def test_unicode_slug_empty_separator(self) -> None:
        assert is_slug("espa\u00f1a", separator="", allow_unicode=True) is True
        assert is_slug("espa\u00f1a mundo", separator="", allow_unicode=True) is False

    def test_emoji_slug_allowed(self) -> None:
        """Regression: is_slug must accept emoji characters when allow_unicode=True."""
        assert is_slug("🎉-party", allow_unicode=True) is True
        assert is_slug("🎉", allow_unicode=True) is True
        assert is_slug("café-🎉-naïve", allow_unicode=True) is True

    def test_emoji_slug_disallowed_in_ascii_mode(self) -> None:
        assert is_slug("🎉-party") is False

    def test_emoji_slug_all_ranges_allowed(self) -> None:
        """Regression: is_slug must accept every emoji range slugify can emit."""
        assert is_slug("hello-⌚-world", allow_unicode=True) is True
        assert is_slug("a-⬆-b", allow_unicode=True) is True
        assert is_slug("⭐-star", allow_unicode=True) is True

    def test_emoji_zwj_sequence_allowed(self) -> None:
        """Regression: is_slug must accept ZWJ emoji sequences."""
        assert is_slug("hi-👨\u200d👩\u200d👧-yo", allow_unicode=True) is True

    def test_emoji_variation_selector_allowed(self) -> None:
        """Regression: is_slug must accept emoji variation selectors (FE0F)."""
        assert is_slug("a-\ufe0f-b", allow_unicode=True) is True

    def test_slugify_emoji_keep_output_validates(self) -> None:
        """Regression: slugify(emoji_mode='keep') output must pass is_slug."""
        from slugany import slugify

        for text in ("hello ⌚ world", "a⬆b", "hi 👨\u200d👩\u200d👧 yo"):
            result = slugify(text, emoji_mode="keep", allow_unicode=True)
            assert is_slug(result, allow_unicode=True), f"invalid slug: {result!r}"

    def test_alphanumeric_separator_raises(self) -> None:
        """Regression: separators with alphanumerics must raise ValueError."""
        with pytest.raises(ValueError, match="alphanumeric"):
            is_slug("aXb", separator="X")
        with pytest.raises(ValueError, match="alphanumeric"):
            is_slug("hello", separator="a1")

    def test_whitespace_separator_raises(self) -> None:
        """Regression: whitespace separators must raise ValueError."""
        with pytest.raises(ValueError, match="whitespace"):
            is_slug("hello world", separator=" ")
        with pytest.raises(ValueError, match="whitespace"):
            is_slug("hello\tworld", separator="\t")

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

    def test_combining_marks_allowed(self) -> None:
        """Regression: is_slug must accept combining marks when allow_unicode=True."""
        assert is_slug("नमस्ते", allow_unicode=True) is True
        assert is_slug("مَرْحَبَا", allow_unicode=True) is True
        assert is_slug("שָׁלוֹם", allow_unicode=True) is True

    def test_combining_marks_with_separator(self) -> None:
        """Regression: is_slug must accept combining marks with separator."""
        assert is_slug("नमस्ते-world", allow_unicode=True) is True
        assert is_slug("नमस्ते", separator="", allow_unicode=True) is True
