from __future__ import annotations

import pytest

from slugany import slugify


class TestSlugify:
    def test_basic(self) -> None:
        assert slugify("Hello World") == "hello-world"

    def test_spanish(self) -> None:
        assert slugify("\u00a1Hola Mundo!", lang="es") == "hola-mundo"

    def test_french(self) -> None:
        assert slugify("Caf\u00e9 r\u00e9sum\u00e9", lang="fr") == "cafe-resume"

    def test_german(self) -> None:
        assert slugify("\u00dcbung Stra\u00dfe", lang="de") == "uebung-strasse"

    def test_portuguese(self) -> None:
        assert slugify("Cora\u00e7\u00e3o", lang="pt") == "coracao"

    def test_custom_separator(self) -> None:
        assert slugify("Hello World", separator="_") == "hello_world"

    def test_no_lowercase(self) -> None:
        assert slugify("Hello World", lowercase=False) == "Hello-World"

    def test_max_length(self) -> None:
        assert slugify("hello-world-foo", max_length=10) == "hello-worl"

    def test_word_boundary(self) -> None:
        assert slugify("hello-world-foo", max_length=10, word_boundary=True) == "hello"

    def test_stopwords(self) -> None:
        assert slugify("the hello world", stopwords=["the"]) == "hello-world"

    def test_fallback(self) -> None:
        assert slugify("!!!", fallback="untitled") == "untitled"

    def test_empty(self) -> None:
        assert slugify("") == ""

    def test_only_punctuation(self) -> None:
        assert slugify("!!!") == ""

    def test_html_entities(self) -> None:
        assert slugify("Bob&amp;Cafe") == "bob-cafe"

    def test_allow_unicode(self) -> None:
        assert slugify("Espa\u00f1a", allow_unicode=True) == "espa\u00f1a"

    def test_replacements(self) -> None:
        assert slugify("hello world", replacements={"hello": "hi"}) == "hi-world"

    def test_emoji_strip(self) -> None:
        assert slugify("Hello \U0001f389 World") == "hello-world"

    def test_style_camel(self) -> None:
        assert slugify("hello world", style="camel") == "helloWorld"

    def test_style_pascal(self) -> None:
        assert slugify("hello world", style="pascal") == "HelloWorld"

    def test_style_filename(self) -> None:
        assert slugify("Hello World", style="filename") == "Hello-World"

    def test_idempotency(self) -> None:
        result = slugify("Hello World!")
        assert slugify(result) == result

    def test_type_error(self) -> None:
        with pytest.raises(TypeError):
            slugify(123)  # type: ignore[arg-type]

    def test_emoji_mode_explicit(self) -> None:
        assert slugify("Hello \U0001f389", emoji_mode="strip") == "hello"

    def test_css_safe(self) -> None:
        assert slugify("123 hello", css_safe=True) == "s-123-hello"

    def test_html_entities_explicit(self) -> None:
        assert slugify("Bob&amp;Cafe", html_entities=True) == "bob-cafe"

    def test_smart_punctuation_explicit(self) -> None:
        assert slugify("Bob\u2019s", smart_punctuation=True) == "bob-s"
