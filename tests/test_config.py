from __future__ import annotations

import pytest

from slugany._config import SlugConfig


class TestSlugConfig:
    def test_defaults(self) -> None:
        c = SlugConfig()
        assert c.separator == "-"
        assert c.lowercase is True
        assert c.max_length == 0
        assert c.word_boundary is False
        assert c.stopwords == frozenset()
        assert c.allow_unicode is False
        assert c.replacements == ()
        assert c.style is None
        assert c.lang == "auto"
        assert c.fallback == ""
        assert c.emoji_mode == "strip"
        assert c.css_safe is False
        assert c.html_entities is True
        assert c.smart_punctuation is True

    def test_custom_separator(self) -> None:
        c = SlugConfig(separator="_")
        assert c.separator == "_"

    def test_frozen(self) -> None:
        c = SlugConfig()
        with pytest.raises(AttributeError):
            c.separator = "_"  # type: ignore[misc]

    def test_from_kwargs_defaults(self) -> None:
        c = SlugConfig.from_kwargs()
        assert c.separator == "-"
        assert c.lowercase is True
        assert c.style is None

    def test_from_kwargs_override(self) -> None:
        c = SlugConfig.from_kwargs(separator="_", lowercase=False)
        assert c.separator == "_"
        assert c.lowercase is False

    def test_from_kwargs_style_url(self) -> None:
        c = SlugConfig.from_kwargs(style="url")
        assert c.separator == "-"
        assert c.lowercase is True

    def test_from_kwargs_style_filename(self) -> None:
        c = SlugConfig.from_kwargs(style="filename")
        assert c.separator == "-"
        assert c.lowercase is False

    def test_from_kwargs_style_override(self) -> None:
        c = SlugConfig.from_kwargs(style="url", separator="_")
        assert c.separator == "_"
        assert c.lowercase is True

    def test_from_kwargs_style_explicit_separator_overrides_preset(self) -> None:
        """Explicitly passing separator='-' with style='snake' overrides preset."""
        c = SlugConfig.from_kwargs(style="snake", separator="-")
        assert c.separator == "-"
        assert c.lowercase is True

    def test_from_kwargs_style_no_separator_uses_preset(self) -> None:
        """Not passing separator with style='snake' uses preset separator."""
        c = SlugConfig.from_kwargs(style="snake")
        assert c.separator == "_"
        assert c.lowercase is True

    def test_from_kwargs_style_explicit_lowercase_overrides_preset(self) -> None:
        """Explicitly passing lowercase=False with style='filename' overrides preset."""
        c = SlugConfig.from_kwargs(style="filename", lowercase=True)
        assert c.separator == "-"
        assert c.lowercase is True

    def test_from_kwargs_style_both_override_preset(self) -> None:
        """Explicitly passing both separator and lowercase overrides preset."""
        c = SlugConfig.from_kwargs(style="snake", separator="-", lowercase=False)
        assert c.separator == "-"
        assert c.lowercase is False

    def test_from_kwargs_style_camel(self) -> None:
        c = SlugConfig.from_kwargs(style="camel")
        assert c.separator == "-"
        assert c.lowercase is False
        assert c.style == "camel"

    def test_from_kwargs_invalid_style(self) -> None:
        with pytest.raises(ValueError, match="Invalid style"):
            SlugConfig.from_kwargs(style="invalid")

    def test_from_kwargs_invalid_lang(self) -> None:
        with pytest.raises(ValueError, match="Invalid lang"):
            SlugConfig.from_kwargs(lang="xx")

    def test_from_kwargs_invalid_emoji(self) -> None:
        with pytest.raises(ValueError, match="Invalid emoji_mode"):
            SlugConfig.from_kwargs(emoji_mode="invalid")

    def test_from_kwargs_empty_separator(self) -> None:
        with pytest.raises(ValueError, match="separator"):
            SlugConfig.from_kwargs(separator="")

    def test_from_kwargs_replacements_dict(self) -> None:
        c = SlugConfig.from_kwargs(replacements={"ll": "2"})
        assert c.replacements == (("ll", "2"),)

    def test_from_kwargs_replacements_iterable(self) -> None:
        c = SlugConfig.from_kwargs(replacements=[("ll", "2"), ("oo", "0")])
        assert c.replacements == (("ll", "2"), ("oo", "0"))

    def test_from_kwargs_replacements_preserves_order(self) -> None:
        c = SlugConfig.from_kwargs(replacements=[("a", "b"), ("b", "c")])
        assert c.replacements == (("a", "b"), ("b", "c"))
        assert c.replacements[0] == ("a", "b")

    def test_from_kwargs_stopwords_list(self) -> None:
        c = SlugConfig.from_kwargs(stopwords=["the", "a"])
        assert c.stopwords == frozenset({"the", "a"})

    def test_from_kwargs_invalid_max_length_type(self) -> None:
        with pytest.raises(TypeError, match="max_length must be an integer"):
            SlugConfig.from_kwargs(max_length="10")  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="max_length must be an integer"):
            SlugConfig.from_kwargs(max_length=3.5)  # type: ignore[arg-type]

    def test_from_kwargs_invalid_fallback_type(self) -> None:
        with pytest.raises(TypeError, match="fallback must be a string"):
            SlugConfig.from_kwargs(fallback=123)  # type: ignore[arg-type]

    def test_from_kwargs_invalid_bool_types(self) -> None:
        for field in (
            "lowercase",
            "word_boundary",
            "allow_unicode",
            "css_safe",
            "html_entities",
            "smart_punctuation",
        ):
            with pytest.raises(TypeError, match=f"{field} must be a boolean"):
                SlugConfig.from_kwargs(**{field: "yes"})  # type: ignore[arg-type]
