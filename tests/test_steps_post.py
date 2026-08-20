from __future__ import annotations

from slugany._config import SlugConfig
from slugany._steps import (
    _apply_case_style,
    _apply_css_safe,
    _apply_fallback,
    _collapse_separators,
    _remove_stopwords,
    _replace_non_alphanumeric,
    _trim_separators,
    _truncate,
)


class TestRemoveStopwords:
    def test_basic(self) -> None:
        cfg = SlugConfig(stopwords=frozenset({"the"}))
        assert _remove_stopwords("the hello world", cfg) == "hello world"

    def test_case_insensitive(self) -> None:
        cfg = SlugConfig(stopwords=frozenset({"THE"}))
        assert _remove_stopwords("the hello world", cfg) == "hello world"

    def test_empty(self) -> None:
        assert _remove_stopwords("hello world", SlugConfig()) == "hello world"

    def test_multiple(self) -> None:
        cfg = SlugConfig(stopwords=frozenset({"the", "a", "is"}))
        assert _remove_stopwords("the a is hello", cfg) == "hello"

    def test_no_match(self) -> None:
        cfg = SlugConfig(stopwords=frozenset({"xyz"}))
        assert _remove_stopwords("hello world", cfg) == "hello world"

    def test_stopword_with_non_alphanumeric(self) -> None:
        """Regression: stopwords containing non-alphanumeric chars must match."""
        cfg = SlugConfig(stopwords=frozenset({"hello-world"}))
        assert _remove_stopwords("hello-world foo", cfg) == "foo"

    def test_stopword_with_underscore(self) -> None:
        """Regression: stopwords with underscores must match after normalization."""
        cfg = SlugConfig(stopwords=frozenset({"hello_world"}))
        assert _remove_stopwords("hello_world foo", cfg) == "foo"

    def test_stopword_auto_lang_german(self) -> None:
        """Regression: lang='auto' must detect language for stopword normalization."""
        cfg = SlugConfig.from_kwargs(stopwords=["\u00e4"], lang="auto")
        assert _remove_stopwords("ae hello", cfg) == "hello"


class TestReplaceNonAlphanumeric:
    def test_basic(self) -> None:
        assert _replace_non_alphanumeric("Hello World!!!", SlugConfig()) == "Hello-World-"

    def test_custom_sep(self) -> None:
        assert (
            _replace_non_alphanumeric("Hello World!!!", SlugConfig(separator="_")) == "Hello_World_"
        )

    def test_unicode(self) -> None:
        assert (
            _replace_non_alphanumeric("Hello World", SlugConfig(allow_unicode=True))
            == "Hello-World"
        )

    def test_all_non_alnum(self) -> None:
        assert _replace_non_alphanumeric("!!!", SlugConfig()) == "-"


class TestCollapseSeparators:
    def test_basic(self) -> None:
        assert _collapse_separators("a---b", SlugConfig()) == "a-b"

    def test_custom(self) -> None:
        assert _collapse_separators("a___b", SlugConfig(separator="_")) == "a_b"

    def test_none(self) -> None:
        assert _collapse_separators("a-b", SlugConfig()) == "a-b"

    def test_empty_separator(self) -> None:
        assert _collapse_separators("a-b", SlugConfig(separator="")) == "a-b"


class TestTrimSeparators:
    def test_basic(self) -> None:
        assert _trim_separators("-hello-world-", SlugConfig()) == "hello-world"

    def test_custom(self) -> None:
        assert _trim_separators("_hello_world_", SlugConfig(separator="_")) == "hello_world"

    def test_none(self) -> None:
        assert _trim_separators("hello-world", SlugConfig()) == "hello-world"

    def test_empty_separator(self) -> None:
        assert _trim_separators("hello-world", SlugConfig(separator="")) == "hello-world"

    def test_partial_trailing_separator(self) -> None:
        assert _trim_separators("æu-", SlugConfig(separator="--")) == "æu"

    def test_partial_leading_separator(self) -> None:
        assert _trim_separators("-æu", SlugConfig(separator="--")) == "æu"

    def test_partial_both_separators(self) -> None:
        assert _trim_separators("-æu-", SlugConfig(separator="--")) == "æu"

    def test_full_separator_still_works(self) -> None:
        assert _trim_separators("--hello--world--", SlugConfig(separator="--")) == "hello--world"


class TestTruncate:
    def test_no_limit(self) -> None:
        assert _truncate("hello-world-foo", SlugConfig()) == "hello-world-foo"

    def test_exact(self) -> None:
        assert _truncate("hello", SlugConfig(max_length=5)) == "hello"

    def test_basic(self) -> None:
        assert _truncate("hello-world-foo", SlugConfig(max_length=10)) == "hello-worl"

    def test_word_boundary(self) -> None:
        cfg = SlugConfig(max_length=10, word_boundary=True)
        assert _truncate("hello-world-foo", cfg) == "hello"

    def test_word_boundary_exact(self) -> None:
        """Regression: word_boundary at exact separator position returns full truncated text."""
        cfg = SlugConfig(max_length=11, word_boundary=True)
        assert _truncate("hello-world-foo", cfg) == "hello-world"

    def test_word_boundary_multi_char_exact(self) -> None:
        """Regression: word_boundary with multi-char separator at exact boundary."""
        cfg = SlugConfig(separator="--", max_length=12, word_boundary=True)
        assert _truncate("hello--world--foo", cfg) == "hello--world"


class TestApplyCaseStyle:
    def test_camel(self) -> None:
        cfg = SlugConfig.from_kwargs(style="camel")
        assert _apply_case_style("hello-world", cfg) == "helloWorld"

    def test_pascal(self) -> None:
        cfg = SlugConfig.from_kwargs(style="pascal")
        assert _apply_case_style("hello-world", cfg) == "HelloWorld"

    def test_train(self) -> None:
        cfg = SlugConfig.from_kwargs(style="train")
        assert _apply_case_style("hello-world", cfg) == "Hello-World"

    def test_no_style(self) -> None:
        assert _apply_case_style("hello-world", SlugConfig()) == "hello-world"

    def test_empty_sep(self) -> None:
        cfg = SlugConfig.from_kwargs(style="camel")
        assert _apply_case_style("hello-world", cfg) == "helloWorld"

    def test_trailing_separator_camel(self) -> None:
        cfg = SlugConfig.from_kwargs(style="camel")
        assert _apply_case_style("hello-", cfg) == "hello"

    def test_trailing_separator_pascal(self) -> None:
        cfg = SlugConfig.from_kwargs(style="pascal")
        assert _apply_case_style("hello-", cfg) == "Hello"

    def test_trailing_separator_train(self) -> None:
        cfg = SlugConfig.from_kwargs(style="train")
        assert _apply_case_style("hello-", cfg) == "Hello"

    def test_leading_separator_camel(self) -> None:
        cfg = SlugConfig.from_kwargs(style="camel")
        assert _apply_case_style("-hello", cfg) == "hello"

    def test_empty_text_camel(self) -> None:
        cfg = SlugConfig.from_kwargs(style="camel")
        assert _apply_case_style("", cfg) == ""

    def test_empty_text_train(self) -> None:
        cfg = SlugConfig.from_kwargs(style="train")
        assert _apply_case_style("", cfg) == ""

    def test_only_separator_train(self) -> None:
        cfg = SlugConfig.from_kwargs(style="train")
        assert _apply_case_style("-", cfg) == ""

    def test_camel_case_boundary_split(self) -> None:
        """Regression: case-boundary splitting for camelCase input without separators."""
        cfg = SlugConfig.from_kwargs(style="camel")
        assert _apply_case_style("helloWorld", cfg) == "helloWorld"

    def test_pascal_case_boundary_split(self) -> None:
        """Regression: case-boundary splitting for PascalCase input without separators."""
        cfg = SlugConfig.from_kwargs(style="pascal")
        assert _apply_case_style("HelloWorld", cfg) == "HelloWorld"

    def test_train_case_boundary_split(self) -> None:
        """Regression: case-boundary splitting for train style input without separators."""
        cfg = SlugConfig.from_kwargs(style="train")
        assert _apply_case_style("helloWorld", cfg) == "Hello-World"

    def test_camel_case_boundary_with_digits(self) -> None:
        """Regression: case-boundary splitting with digits."""
        cfg = SlugConfig.from_kwargs(style="camel")
        assert _apply_case_style("hello123World", cfg) == "hello123World"

    def test_camel_upper_upper_lower_split(self) -> None:
        """Cover Upper->Upper+lower boundary: 'ABCdef' -> 'A', 'B', 'Cdef' -> camel 'aBCdef'."""
        cfg = SlugConfig.from_kwargs(style="camel")
        assert _apply_case_style("ABCdef", cfg) == "aBCdef"

    def test_split_case_boundaries_empty(self) -> None:
        """Cover empty word edge case in _split_case_boundaries."""
        from slugany._steps import _split_case_boundaries

        assert _split_case_boundaries("") == []

    def test_split_case_boundaries_caseless_alpha_uppercase(self) -> None:
        """Regression: caseless alpha (CJK) followed by uppercase must split."""
        from slugany._steps import _split_case_boundaries

        assert _split_case_boundaries("こWorld") == ["こ", "World"]
        assert _split_case_boundaries("abc你好World") == ["abc你好", "World"]


class TestCaseStyles:
    def test_camel(self) -> None:
        cfg = SlugConfig.from_kwargs(style="camel")
        assert _apply_case_style("hello-world", cfg) == "helloWorld"

    def test_pascal(self) -> None:
        cfg = SlugConfig.from_kwargs(style="pascal")
        assert _apply_case_style("hello-world", cfg) == "HelloWorld"

    def test_train(self) -> None:
        cfg = SlugConfig.from_kwargs(style="train")
        assert _apply_case_style("hello-world", cfg) == "Hello-World"

    def test_no_style(self) -> None:
        assert _apply_case_style("hello-world", SlugConfig()) == "hello-world"

    def test_empty_separator(self) -> None:
        cfg = SlugConfig(style="camel", separator="")
        assert _apply_case_style("helloworld", cfg) == "helloworld"


class TestApplyFallback:
    def test_empty(self) -> None:
        assert _apply_fallback("", SlugConfig(fallback="untitled")) == "untitled"

    def test_non_empty(self) -> None:
        assert _apply_fallback("hello", SlugConfig(fallback="untitled")) == "hello"

    def test_no_fallback(self) -> None:
        assert _apply_fallback("", SlugConfig()) == ""


class TestApplyCssSafe:
    def test_not_css_safe(self) -> None:
        assert _apply_css_safe("123hello", SlugConfig()) == "123hello"

    def test_starts_with_letter(self) -> None:
        cfg = SlugConfig(css_safe=True)
        assert _apply_css_safe("hello", cfg) == "hello"

    def test_empty(self) -> None:
        assert _apply_css_safe("", SlugConfig(css_safe=True)) == ""

    def test_default_style(self) -> None:
        cfg = SlugConfig(css_safe=True)
        assert _apply_css_safe("123hello", cfg) == "s-123hello"

    def test_camel_style(self) -> None:
        """Regression: css_safe with camel prepends 's' without separator."""
        cfg = SlugConfig.from_kwargs(css_safe=True, style="camel")
        assert _apply_css_safe("123Hello", cfg) == "s123Hello"

    def test_pascal_style(self) -> None:
        """Regression: css_safe with pascal prepends 'S' without separator."""
        cfg = SlugConfig.from_kwargs(css_safe=True, style="pascal")
        assert _apply_css_safe("123Hello", cfg) == "S123Hello"

    def test_train_style(self) -> None:
        """Regression: css_safe with train prepends 'S' with separator."""
        cfg = SlugConfig.from_kwargs(css_safe=True, style="train")
        assert _apply_css_safe("123-Hello", cfg) == "S-123-Hello"


class TestCssSafe:
    def test_starts_with_digit(self) -> None:
        cfg = SlugConfig(css_safe=True)
        assert _apply_css_safe("2024-recap", cfg) == "s-2024-recap"

    def test_no_digit(self) -> None:
        cfg = SlugConfig(css_safe=True)
        assert _apply_css_safe("hello-world", cfg) == "hello-world"

    def test_css_safe_false(self) -> None:
        cfg = SlugConfig(css_safe=False)
        assert _apply_css_safe("2024-recap", cfg) == "2024-recap"
