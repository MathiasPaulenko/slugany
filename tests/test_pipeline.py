from __future__ import annotations

from slugany._config import SlugConfig
from slugany._pipeline import _run_pipeline


class TestPipeline:
    def test_basic_spanish(self) -> None:
        assert _run_pipeline("\u00a1Hola Mundo!", SlugConfig()) == "hola-mundo"

    def test_basic_french(self) -> None:
        assert _run_pipeline("Caf\u00e9 r\u00e9sum\u00e9", SlugConfig()) == "cafe-resume"

    def test_basic_german(self) -> None:
        assert _run_pipeline("\u00dcbung Stra\u00dfe", SlugConfig(lang="de")) == "uebung-strasse"

    def test_empty(self) -> None:
        assert _run_pipeline("", SlugConfig()) == ""

    def test_only_punctuation(self) -> None:
        assert _run_pipeline("!!!", SlugConfig()) == ""

    def test_fallback(self) -> None:
        assert _run_pipeline("!!!", SlugConfig(fallback="untitled")) == "untitled"

    def test_custom_separator(self) -> None:
        assert _run_pipeline("Hello World", SlugConfig(separator="_")) == "hello_world"

    def test_no_lowercase(self) -> None:
        assert _run_pipeline("Hello World", SlugConfig(lowercase=False)) == "Hello-World"

    def test_max_length(self) -> None:
        assert _run_pipeline("hello-world-foo", SlugConfig(max_length=10)) == "hello-worl"

    def test_word_boundary(self) -> None:
        cfg = SlugConfig(max_length=10, word_boundary=True)
        assert _run_pipeline("hello-world-foo", cfg) == "hello"

    def test_stopwords(self) -> None:
        cfg = SlugConfig(stopwords=frozenset({"the"}))
        assert _run_pipeline("the hello world", cfg) == "hello-world"

    def test_html_entities(self) -> None:
        assert _run_pipeline("Bob&amp;Cafe", SlugConfig()) == "bob-cafe"

    def test_smart_punctuation(self) -> None:
        assert _run_pipeline("Bob\u2019s caf\u00e9", SlugConfig()) == "bob-s-cafe"

    def test_allow_unicode(self) -> None:
        assert _run_pipeline("Espa\u00f1a", SlugConfig(allow_unicode=True)) == "espa\u00f1a"

    def test_replacements(self) -> None:
        cfg = SlugConfig.from_kwargs(replacements={"hello": "hi"})
        assert _run_pipeline("hello world", cfg) == "hi-world"

    def test_emoji_strip(self) -> None:
        assert _run_pipeline("Hello \U0001f389 World", SlugConfig()) == "hello-world"

    def test_css_safe(self) -> None:
        cfg = SlugConfig(css_safe=True)
        assert _run_pipeline("123 hello", cfg) == "s-123-hello"

    def test_css_safe_not_triggered(self) -> None:
        cfg = SlugConfig(css_safe=True)
        assert _run_pipeline("hello 123", cfg) == "hello-123"

    def test_case_style_camel(self) -> None:
        cfg = SlugConfig.from_kwargs(style="camel")
        assert _run_pipeline("hello world", cfg) == "helloWorld"

    def test_case_style_train(self) -> None:
        cfg = SlugConfig.from_kwargs(style="train")
        assert _run_pipeline("hello world", cfg) == "Hello-World"

    def test_confusables(self) -> None:
        assert _run_pipeline("\u0441afe", SlugConfig()) == "cafe"

    def test_short_circuit_empty(self) -> None:
        assert _run_pipeline("!!!", SlugConfig(fallback="fb")) == "fb"

    def test_short_circuit_no_fallback(self) -> None:
        assert _run_pipeline("!!!", SlugConfig()) == ""

    def test_post_replacement_after_lowercase(self) -> None:
        """Regression: post-replacements must run after lowercase."""
        cfg = SlugConfig.from_kwargs(replacements={"hello": "X"})
        assert _run_pipeline("HELLO", cfg) == "x"
