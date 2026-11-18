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

    def test_from_kwargs_alphanumeric_separator(self) -> None:
        """Regression: alphanumeric separators corrupt content via _collapse_separators."""
        with pytest.raises(ValueError, match="alphanumeric"):
            SlugConfig.from_kwargs(separator="ab")
        with pytest.raises(ValueError, match="alphanumeric"):
            SlugConfig.from_kwargs(separator="x")
        with pytest.raises(ValueError, match="alphanumeric"):
            SlugConfig.from_kwargs(separator="a1")

    def test_from_kwargs_whitespace_separator(self) -> None:
        """Regression: whitespace separators produce invalid slugs and must be rejected."""
        with pytest.raises(ValueError, match="whitespace"):
            SlugConfig.from_kwargs(separator=" ")
        with pytest.raises(ValueError, match="whitespace"):
            SlugConfig.from_kwargs(separator="\t")
        with pytest.raises(ValueError, match="whitespace"):
            SlugConfig.from_kwargs(separator="- -")

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

    def test_from_kwargs_max_length_rejects_bool(self) -> None:
        """Regression: bool is a subclass of int but must be rejected for max_length."""
        with pytest.raises(TypeError, match="max_length must be an integer"):
            SlugConfig.from_kwargs(max_length=True)  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="max_length must be an integer"):
            SlugConfig.from_kwargs(max_length=False)  # type: ignore[arg-type]

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


class TestSlugConfigPostInit:
    """Direct construction must be validated like from_kwargs."""

    def test_direct_alphanumeric_separator_rejected(self) -> None:
        with pytest.raises(ValueError, match="alphanumeric"):
            SlugConfig(separator="ab")

    def test_direct_whitespace_separator_rejected(self) -> None:
        with pytest.raises(ValueError, match="whitespace"):
            SlugConfig(separator=" ")

    def test_direct_empty_separator_allowed(self) -> None:
        """Empty separator is a supported advanced value for direct construction."""
        assert SlugConfig(separator="").separator == ""

    def test_direct_non_string_separator_rejected(self) -> None:
        with pytest.raises(TypeError, match="separator must be a string"):
            SlugConfig(separator=5)  # type: ignore[arg-type]

    def test_direct_negative_max_length_rejected(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            SlugConfig(max_length=-1)

    def test_direct_invalid_max_length_type_rejected(self) -> None:
        with pytest.raises(TypeError, match="max_length must be an integer"):
            SlugConfig(max_length="10")  # type: ignore[arg-type]
        with pytest.raises(TypeError, match="max_length must be an integer"):
            SlugConfig(max_length=True)  # type: ignore[arg-type]

    def test_direct_invalid_bool_rejected(self) -> None:
        with pytest.raises(TypeError, match="lowercase must be a boolean"):
            SlugConfig(lowercase="yes")  # type: ignore[arg-type]

    def test_direct_invalid_fallback_rejected(self) -> None:
        with pytest.raises(TypeError, match="fallback must be a string"):
            SlugConfig(fallback=1)  # type: ignore[arg-type]

    def test_direct_invalid_style_rejected(self) -> None:
        with pytest.raises(ValueError, match="Invalid style"):
            SlugConfig(style="nope")
        with pytest.raises(TypeError, match="style must be a string"):
            SlugConfig(style=1)  # type: ignore[arg-type]

    def test_direct_invalid_lang_rejected(self) -> None:
        with pytest.raises(ValueError, match="Invalid lang"):
            SlugConfig(lang="xx")
        with pytest.raises(TypeError, match="lang must be a string"):
            SlugConfig(lang=["es"])  # type: ignore[arg-type]

    def test_direct_invalid_emoji_mode_rejected(self) -> None:
        with pytest.raises(ValueError, match="Invalid emoji_mode"):
            SlugConfig(emoji_mode="x")

    def test_direct_stopwords_coerced_to_frozenset(self) -> None:
        assert SlugConfig(stopwords=["the"]).stopwords == frozenset({"the"})
        assert SlugConfig(stopwords=("the",)).stopwords == frozenset({"the"})

    def test_direct_stopwords_non_string_entry_rejected(self) -> None:
        with pytest.raises(TypeError, match="stopwords entries must be strings"):
            SlugConfig(stopwords=["the", 2])  # type: ignore[list-item]

    def test_direct_stopwords_bare_string_rejected(self) -> None:
        with pytest.raises(TypeError, match="bare string"):
            SlugConfig(stopwords="the")  # type: ignore[arg-type]

    def test_direct_stopwords_mapping_rejected(self) -> None:
        with pytest.raises(TypeError, match="stopwords must be an iterable of strings"):
            SlugConfig(stopwords={"the": 1})  # type: ignore[arg-type]

    def test_direct_stopwords_non_iterable_rejected(self) -> None:
        with pytest.raises(TypeError, match="stopwords must be an iterable of strings"):
            SlugConfig(stopwords=5)  # type: ignore[arg-type]

    def test_direct_replacements_coerced(self) -> None:
        assert SlugConfig(replacements=[("a", "b")]).replacements == (("a", "b"),)
        assert SlugConfig(replacements={"a": "b"}).replacements == (("a", "b"),)

    def test_direct_replacements_set_rejected(self) -> None:
        """Regression: set iteration order is not deterministic across processes."""
        with pytest.raises(TypeError, match="not deterministic"):
            SlugConfig(replacements={("a", "b")})  # type: ignore[arg-type]

    def test_direct_replacements_bare_string_rejected(self) -> None:
        with pytest.raises(TypeError, match="bare string"):
            SlugConfig(replacements="ab")  # type: ignore[arg-type]

    def test_direct_replacements_non_iterable_rejected(self) -> None:
        with pytest.raises(TypeError, match="replacements must be a mapping or an iterable"):
            SlugConfig(replacements=5)  # type: ignore[arg-type]

    def test_direct_replacements_bad_pair_rejected(self) -> None:
        with pytest.raises(TypeError, match="replacements entries must be"):
            SlugConfig(replacements=[("a",)])  # type: ignore[list-item]
        with pytest.raises(TypeError, match="replacements keys and values must be strings"):
            SlugConfig(replacements=[("a", 1)])  # type: ignore[list-item]
        with pytest.raises(ValueError, match="replacements keys must be non-empty"):
            SlugConfig(replacements=[("", "b")])

    def test_from_kwargs_negative_max_length_rejected(self) -> None:
        with pytest.raises(ValueError, match="non-negative"):
            SlugConfig.from_kwargs(max_length=-5)

    def test_from_kwargs_stopwords_non_string_entry_rejected(self) -> None:
        with pytest.raises(TypeError, match="stopwords entries must be strings"):
            SlugConfig.from_kwargs(stopwords=[1, 2])  # type: ignore[list-item]

    def test_from_kwargs_stopwords_bare_string_rejected(self) -> None:
        with pytest.raises(TypeError, match="bare string"):
            SlugConfig.from_kwargs(stopwords="he")  # type: ignore[arg-type]

    def test_from_kwargs_replacements_set_rejected(self) -> None:
        with pytest.raises(TypeError, match="not deterministic"):
            SlugConfig.from_kwargs(replacements={("a", "b")})  # type: ignore[arg-type]

    def test_from_kwargs_non_string_style_rejected(self) -> None:
        with pytest.raises(TypeError, match="style must be a string"):
            SlugConfig.from_kwargs(style=["camel"])  # type: ignore[arg-type]

    def test_from_kwargs_non_string_lang_rejected(self) -> None:
        with pytest.raises(TypeError, match="lang must be a string"):
            SlugConfig.from_kwargs(lang=["es"])  # type: ignore[arg-type]

    def test_from_kwargs_non_string_emoji_mode_rejected(self) -> None:
        with pytest.raises(TypeError, match="emoji_mode must be a string"):
            SlugConfig.from_kwargs(emoji_mode=["strip"])  # type: ignore[arg-type]

    def test_from_kwargs_non_string_separator_rejected(self) -> None:
        with pytest.raises(TypeError, match="separator must be a string"):
            SlugConfig.from_kwargs(separator=5)  # type: ignore[arg-type]


class TestFromKwargsNoneMeansDefault:
    """Regression: explicit None kwargs must fall back to defaults.

    Previously max_length=None crashed deep in the pipeline, and
    html_entities=None / smart_punctuation=None silently disabled their
    features instead of using the defaults.
    """

    def test_max_length_none(self) -> None:
        assert SlugConfig.from_kwargs(max_length=None).max_length == 0

    def test_html_entities_none(self) -> None:
        assert SlugConfig.from_kwargs(html_entities=None).html_entities is True

    def test_smart_punctuation_none(self) -> None:
        assert SlugConfig.from_kwargs(smart_punctuation=None).smart_punctuation is True

    def test_word_boundary_none(self) -> None:
        assert SlugConfig.from_kwargs(word_boundary=None).word_boundary is False

    def test_allow_unicode_none(self) -> None:
        assert SlugConfig.from_kwargs(allow_unicode=None).allow_unicode is False

    def test_css_safe_none(self) -> None:
        assert SlugConfig.from_kwargs(css_safe=None).css_safe is False

    def test_fallback_none(self) -> None:
        assert SlugConfig.from_kwargs(fallback=None).fallback == ""

    def test_lang_none(self) -> None:
        assert SlugConfig.from_kwargs(lang=None).lang == "auto"

    def test_emoji_mode_none(self) -> None:
        assert SlugConfig.from_kwargs(emoji_mode=None).emoji_mode == "strip"

    def test_stopwords_none(self) -> None:
        assert SlugConfig.from_kwargs(stopwords=None).stopwords == frozenset()

    def test_replacements_none(self) -> None:
        assert SlugConfig.from_kwargs(replacements=None).replacements == ()

    def test_none_with_style_uses_preset(self) -> None:
        c = SlugConfig.from_kwargs(style="snake", separator=None, lowercase=None)
        assert c.separator == "_"
        assert c.lowercase is True
