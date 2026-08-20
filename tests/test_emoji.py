from __future__ import annotations

import pytest

from slugany import slugify
from slugany._config import SlugConfig
from slugany._steps import _handle_emoji


class TestEmojiStrip:
    def test_basic(self) -> None:
        assert _handle_emoji("Hello 🎉 World", SlugConfig()) == "Hello  World"

    def test_multiple(self) -> None:
        assert _handle_emoji("Hello 🎉🔥 World", SlugConfig()) == "Hello  World"

    def test_no_emoji(self) -> None:
        assert _handle_emoji("Hello World", SlugConfig()) == "Hello World"


class TestEmojiText:
    def test_basic(self) -> None:
        result = _handle_emoji("Hello 🎉 World", SlugConfig(emoji_mode="text"))
        assert result == "Hello party-popper World"

    def test_not_in_table(self) -> None:
        result = _handle_emoji("Hello \U0001fa00 World", SlugConfig(emoji_mode="text"))
        assert result == "Hello  World"

    def test_multiple(self) -> None:
        result = _handle_emoji("Hello 🎉🔥 World", SlugConfig(emoji_mode="text"))
        assert result == "Hello party-popper fire World"

    def test_adjacent_emoji_text_mode(self) -> None:
        """Regression: adjacent emojis in text mode must be space-separated."""
        assert slugify("🎉🎊", emoji_mode="text") == "party-popper-confetti-ball"
        assert slugify("🎉🎉", emoji_mode="text") == "party-popper-party-popper"


class TestEmojiKeep:
    def test_with_allow_unicode(self) -> None:
        cfg = SlugConfig(emoji_mode="keep", allow_unicode=True)
        assert _handle_emoji("Hello 🎉", cfg) == "Hello 🎉"

    def test_without_allow_unicode_raises(self) -> None:
        cfg = SlugConfig(emoji_mode="keep", allow_unicode=False)
        with pytest.raises(ValueError, match="allow_unicode=True"):
            _handle_emoji("Hello 🎉", cfg)


class TestEmojiMixed:
    def test_emoji_with_unicode_text(self) -> None:
        result = slugify("Café 🎉 résumé", emoji_mode="text")
        assert result == "cafe-party-popper-resume"

    def test_emoji_strip_with_unicode(self) -> None:
        result = slugify("Café 🎉 résumé", emoji_mode="strip")
        assert result == "cafe-resume"

    def test_emoji_keep_with_unicode(self) -> None:
        result = slugify("Café 🎉 résumé", emoji_mode="keep", allow_unicode=True)
        assert "🎉" in result
        assert "café" in result

    def test_zwj_emoji_sequence_preserved(self) -> None:
        """Regression: ZWJ emoji sequences must be preserved in keep mode."""
        result = slugify("hello 👨\u200d👩\u200d👧 world", emoji_mode="keep", allow_unicode=True)
        assert "\u200d" in result
        assert "👨\u200d👩\u200d👧" in result

    def test_zwj_emoji_sequence_stripped_in_text_mode(self) -> None:
        """Regression: ZWJ must be removed in text mode (emojis replaced)."""
        result = slugify("hello 👨\u200d👩\u200d👧 world", emoji_mode="text")
        assert "\u200d" not in result

    def test_zwj_emoji_sequence_stripped_in_strip_mode(self) -> None:
        """Regression: ZWJ must be removed in strip mode."""
        result = slugify("hello 👨\u200d👩\u200d👧 world", emoji_mode="strip")
        assert "\u200d" not in result

    def test_zwj_stripped_in_default_mode(self) -> None:
        """Regression: ZWJ must be removed in default (strip) mode."""
        result = slugify("hello\u200dworld")
        assert "\u200d" not in result


class TestEmojiUnknownMode:
    def test_unknown_mode_returns_text(self) -> None:
        cfg = SlugConfig(emoji_mode="unknown")
        assert _handle_emoji("Hello 🎉 World", cfg) == "Hello 🎉 World"
