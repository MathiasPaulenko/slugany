from __future__ import annotations

from slugany._config import SlugConfig
from slugany._steps import (
    _apply_case_style,
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


class TestApplyFallback:
    def test_empty(self) -> None:
        assert _apply_fallback("", SlugConfig(fallback="untitled")) == "untitled"

    def test_non_empty(self) -> None:
        assert _apply_fallback("hello", SlugConfig(fallback="untitled")) == "hello"

    def test_no_fallback(self) -> None:
        assert _apply_fallback("", SlugConfig()) == ""
