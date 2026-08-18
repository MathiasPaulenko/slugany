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

    def test_stopwords_case_insensitive(self) -> None:
        assert slugify("The Hello World", stopwords=["the"]) == "hello-world"

    def test_stopwords_all_removed(self) -> None:
        assert slugify("the a", stopwords=["the", "a"]) == ""

    def test_stopwords_with_fallback(self) -> None:
        assert slugify("the a", stopwords=["the", "a"], fallback="empty") == "empty"

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

    def test_style_train(self) -> None:
        assert slugify("hello world", style="train") == "Hello-World"

    def test_style_train_custom_separator(self) -> None:
        assert slugify("hello world", style="train", separator="_") == "Hello_World"

    def test_style_camel_custom_separator(self) -> None:
        assert slugify("hello world", style="camel", separator="_") == "helloWorld"

    def test_style_pascal_custom_separator(self) -> None:
        assert slugify("hello world", style="pascal", separator="_") == "HelloWorld"

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

    def test_newline_tab(self) -> None:
        assert slugify("hello\nworld\tfoo") == "hello-world-foo"

    def test_css_safe_with_fallback(self) -> None:
        assert slugify("!!!", css_safe=True, fallback="123") == "s-123"

    def test_css_safe_not_triggered(self) -> None:
        assert slugify("hello 123", css_safe=True) == "hello-123"

    def test_multi_char_separator(self) -> None:
        assert slugify("hello world", separator="---") == "hello---world"

    def test_style_kebab(self) -> None:
        assert slugify("hello world", style="kebab") == "hello-world"

    def test_style_snake(self) -> None:
        assert slugify("hello world", style="snake") == "hello_world"

    def test_style_dot(self) -> None:
        assert slugify("hello world", style="dot") == "hello.world"

    def test_style_url(self) -> None:
        assert slugify("hello world", style="url") == "hello-world"

    def test_replacements_iterable(self) -> None:
        assert slugify("hello world", replacements=[("hello", "hi")]) == "hi-world"

    def test_replacements_order_matters(self) -> None:
        r1 = [("a", "\u00fc"), ("\u00fc", "u")]
        r2 = [("\u00fc", "u"), ("a", "\u00fc")]
        assert slugify("a", replacements=r1, lang="de") == "u"
        assert slugify("a", replacements=r2, lang="de") == "ue"

    def test_replacements_chained(self) -> None:
        assert slugify("abc", replacements=[("a", "b"), ("b", "c")]) == "ccc"

    def test_truncate_with_style_no_trailing_sep(self) -> None:
        assert slugify("hello-world-foo", style="train", max_length=6) == "Hello"
        assert slugify("hello-world-foo", style="camel", max_length=6) == "hello"
        assert slugify("hello-world-foo", style="pascal", max_length=6) == "Hello"

    def test_truncate_no_trailing_separator(self) -> None:
        s = slugify("hello-world-foo", max_length=6)
        assert s == "hello"
        assert not s.endswith("-")

    def test_truncate_produces_valid_slug(self) -> None:
        from slugany import is_slug

        for n in range(1, 20):
            s = slugify("hello-world-foo-bar", max_length=n)
            assert is_slug(s), f"max_length={n} produced invalid slug: {s!r}"

    def test_truncate_multi_char_separator_no_partial(self) -> None:
        from slugany import is_slug

        for n in range(1, 20):
            s = slugify("hello-world-foo-bar", separator="--", max_length=n)
            assert is_slug(s, separator="--"), f"max_length={n} produced invalid slug: {s!r}"

    def test_invalid_separator_raises(self) -> None:
        with pytest.raises(ValueError, match="separator"):
            slugify("hello", separator="")

    def test_ss_transliteration_auto(self) -> None:
        assert slugify("Straße", lang="auto") == "strasse"

    def test_oe_transliteration_auto(self) -> None:
        assert slugify("Cœur", lang="auto") == "coeur"

    def test_ae_transliteration_auto(self) -> None:
        assert slugify("Ælfred", lang="auto") == "aelfred"
