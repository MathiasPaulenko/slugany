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

    def test_word_boundary_exact_boundary(self) -> None:
        """Regression: word_boundary at exact separator position keeps full word."""
        assert slugify("hello-world-foo", max_length=11, word_boundary=True) == "hello-world"

    def test_word_boundary_leading_separator(self) -> None:
        """Regression: leading separators must not eat into max_length budget."""
        assert slugify("-hello-world", max_length=5, word_boundary=True) == "hello"
        assert slugify("-hello-world", max_length=11, word_boundary=True) == "hello-world"
        assert slugify("-hello-", max_length=5, word_boundary=True) == "hello"

    def test_word_boundary_multi_char_separator(self) -> None:
        """Regression: word_boundary with multi-char separator must not cut mid-separator."""
        assert (
            slugify("hello--world--foo", separator="--", max_length=13, word_boundary=True)
            == "hello--world"
        )
        assert (
            slugify("hello--world--foo", separator="--", max_length=12, word_boundary=True)
            == "hello--world"
        )
        assert (
            slugify("hello--world--foo", separator="--", max_length=5, word_boundary=True)
            == "hello"
        )
        assert (
            slugify("hello--world--foo", separator="--", max_length=17, word_boundary=True)
            == "hello--world--foo"
        )

    def test_stopwords(self) -> None:
        assert slugify("the hello world", stopwords=["the"]) == "hello-world"

    def test_stopwords_case_insensitive(self) -> None:
        assert slugify("The Hello World", stopwords=["the"]) == "hello-world"

    def test_stopwords_all_removed(self) -> None:
        assert slugify("the a", stopwords=["the", "a"]) == ""

    def test_stopwords_with_fallback(self) -> None:
        assert slugify("the a", stopwords=["the", "a"], fallback="empty") == "empty"

    def test_stopwords_with_punctuation(self) -> None:
        """Regression: stopwords must match words with attached punctuation."""
        assert slugify("hello, world", stopwords=["hello"]) == "world"
        assert slugify("hello. world", stopwords=["hello"]) == "world"
        assert slugify("hello! world", stopwords=["hello"]) == "world"
        assert slugify("(hello) world", stopwords=["hello"]) == "world"

    def test_stopwords_with_punctuation_case_insensitive(self) -> None:
        """Regression: stopwords match words with punctuation, case insensitive."""
        assert slugify("Hello, World", stopwords=["hello"]) == "world"
        assert slugify("HELLO! World", stopwords=["hello"]) == "world"

    def test_stopwords_multiple_with_punctuation(self) -> None:
        """Regression: multiple stopwords with punctuation."""
        assert slugify("hello, world, foo", stopwords=["hello", "world"]) == "foo"

    def test_stopwords_with_homoglyphs(self) -> None:
        """Regression: stopwords with Cyrillic homoglyphs must match deconfused text."""
        result = slugify("\u0441afe hello", stopwords=["\u0441afe"])
        assert result == "hello"

    def test_stopwords_unicode_with_punctuation(self) -> None:
        """Regression: unicode stopwords with punctuation and allow_unicode."""
        assert slugify("café, world", stopwords=["café"], allow_unicode=True) == "world"

    def test_fallback(self) -> None:
        assert slugify("!!!", fallback="untitled") == "untitled"

    def test_fallback_normalizes_spaces(self) -> None:
        """Regression: fallback with spaces must produce a valid slug."""
        assert slugify("!!!", fallback="hello world") == "hello-world"

    def test_fallback_normalizes_special_chars(self) -> None:
        """Regression: fallback with special chars must produce a valid slug."""
        assert slugify("!!!", fallback="hello@world") == "hello-world"

    def test_fallback_normalizes_case(self) -> None:
        """Regression: fallback must be lowercased when lowercase=True."""
        assert slugify("!!!", fallback="UPPER CASE") == "upper-case"

    def test_fallback_normalizes_collapses_separators(self) -> None:
        """Regression: fallback with repeated separators must collapse."""
        assert slugify("!!!", fallback="hello--world") == "hello-world"

    def test_fallback_normalizes_trims_separators(self) -> None:
        """Regression: fallback with leading/trailing separators must trim."""
        assert slugify("!!!", fallback="  hello  ") == "hello"

    def test_fallback_with_style(self) -> None:
        """Regression: fallback must be normalized before style is applied."""
        assert slugify("!!!", fallback="hello world", style="camel") == "helloWorld"
        assert slugify("!!!", fallback="hello world", style="pascal") == "HelloWorld"
        assert slugify("!!!", fallback="hello world", style="train") == "Hello-World"

    def test_fallback_with_max_length(self) -> None:
        """Regression: fallback must be truncated to max_length."""
        assert slugify("!!!", fallback="hello-world-foo", max_length=5) == "hello"

    def test_fallback_transliterated(self) -> None:
        """Regression: fallback with non-ASCII must be transliterated."""
        assert slugify("!!!", fallback="café naïve") == "cafe-naive"
        assert slugify("!!!", fallback="café naïve", allow_unicode=True) == "café-naïve"
        assert slugify("!!!", fallback="saße", lang="de") == "sasse"

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

    def test_style_preset_explicit_default_separator_overrides(self) -> None:
        """Regression: explicitly passing separator='-' overrides style preset."""
        assert slugify("hello world", style="snake", separator="-") == "hello-world"
        assert slugify("hello world", style="dot", separator="-") == "hello-world"

    def test_style_preset_explicit_default_lowercase_overrides(self) -> None:
        """Regression: explicitly passing lowercase=True overrides style preset."""
        assert slugify("Hello World", style="filename", lowercase=True) == "hello-world"
        assert slugify("hello world", style="train", lowercase=True) == "Hello-World"

    def test_style_preset_omitted_separator_uses_preset(self) -> None:
        """When separator is not passed, the style preset's separator is used."""
        assert slugify("hello world", style="snake") == "hello_world"
        assert slugify("hello world", style="dot") == "hello.world"

    def test_style_preset_omitted_lowercase_uses_preset(self) -> None:
        """When lowercase is not passed, the style preset's lowercase setting is used."""
        assert slugify("Hello World", style="filename") == "Hello-World"
        assert slugify("hello world", style="train") == "Hello-World"

    def test_idempotency(self) -> None:
        result = slugify("Hello World!")
        assert slugify(result) == result

    def test_type_error(self) -> None:
        with pytest.raises(TypeError):
            slugify(123)  # type: ignore[arg-type]

    def test_emoji_mode_explicit(self) -> None:
        assert slugify("Hello \U0001f389", emoji_mode="strip") == "hello"

    def test_emoji_mode_keep_preserves_emoji(self) -> None:
        """Regression: emoji_mode='keep' must preserve emojis with allow_unicode."""
        result = slugify("Hello\U0001f389World", emoji_mode="keep", allow_unicode=True)
        assert result == "hello-\U0001f389-world"

    def test_emoji_mode_keep_leading_emoji(self) -> None:
        """Regression: emoji_mode='keep' with leading emoji."""
        result = slugify("\U0001f389Hello", emoji_mode="keep", allow_unicode=True)
        assert result == "\U0001f389-hello"

    def test_emoji_mode_keep_trailing_emoji(self) -> None:
        """Regression: emoji_mode='keep' with trailing emoji."""
        result = slugify("Hello\U0001f389", emoji_mode="keep", allow_unicode=True)
        assert result == "hello-\U0001f389"

    def test_emoji_mode_keep_multiple_emojis(self) -> None:
        """Regression: emoji_mode='keep' with consecutive emojis."""
        result = slugify("Hello\U0001f389\U0001f600World", emoji_mode="keep", allow_unicode=True)
        assert result == "hello-\U0001f389\U0001f600-world"

    def test_emoji_mode_keep_without_unicode_raises(self) -> None:
        """emoji_mode='keep' without allow_unicode raises ValueError."""
        with pytest.raises(ValueError, match="allow_unicode=True"):
            slugify("Hello\U0001f389World", emoji_mode="keep")

    def test_emoji_mode_text_replaces_emoji(self) -> None:
        """emoji_mode='text' replaces emojis with text descriptions."""
        result = slugify("Hello\U0001f389World", emoji_mode="text")
        assert result == "helloparty-popperworld"

    def test_css_safe(self) -> None:
        assert slugify("123 hello", css_safe=True) == "s-123-hello"

    def test_css_safe_2024_recap(self) -> None:
        assert slugify("2024 recap", css_safe=True) == "s-2024-recap"

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
        r1 = [("a", "b"), ("b", "c")]
        r2 = [("b", "c"), ("a", "b")]
        assert slugify("a", replacements=r1) == "c"
        assert slugify("a", replacements=r2) == "b"

    def test_replacements_chained(self) -> None:
        assert slugify("abc", replacements=[("a", "b"), ("b", "c")]) == "ccc"

    def test_replacements_empty_key_raises(self) -> None:
        """Regression: empty string keys in replacements must raise ValueError."""
        with pytest.raises(ValueError, match="replacements keys must be non-empty"):
            slugify("hello world", replacements={"": "x"})
        with pytest.raises(ValueError, match="replacements keys must be non-empty"):
            slugify("hello world", replacements=[("", "x")])

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

    def test_collapse_multi_char_separator(self) -> None:
        """Multi-char separators with repeated instances must collapse correctly."""
        result = slugify("hello", replacements={"hello": "foo--bar"}, separator="--")
        assert result == "foo--bar"

    def test_trim_multi_char_separator_leading(self) -> None:
        """Repeated multi-char separator at start must trim fully."""
        result = slugify("xyz", replacements={"xyz": "----hello"}, separator="--")
        assert result == "hello"

    def test_trim_multi_char_separator_trailing(self) -> None:
        """Repeated multi-char separator at end must trim fully."""
        result = slugify("hello", replacements={"hello": "hello----"}, separator="--")
        assert result == "hello"

    def test_collapse_multi_char_separator_both_sides(self) -> None:
        """Collapse and trim multi-char separator from both sides."""
        result = slugify("x", replacements={"x": "----hello----"}, separator="--")
        assert result == "hello"

    def test_collapse_single_char_separator_still_works(self) -> None:
        """Ensure the fix doesn't break single-char separator collapse."""
        assert slugify("hello---world") == "hello-world"
        assert slugify("---hello---") == "hello"

    def test_collapse_multi_char_same_char_separator_still_works(self) -> None:
        """Ensure multi-char separators with same char still work."""
        result = slugify("hello----world", separator="--")
        assert result == "hello--world"
        result = slugify("--hello--", separator="--")
        assert result == "hello"

    def test_invalid_separator_raises(self) -> None:
        with pytest.raises(ValueError, match="separator"):
            slugify("hello", separator="")

    def test_alphanumeric_separator_raises(self) -> None:
        """Regression: alphanumeric separators corrupt content and must be rejected."""
        with pytest.raises(ValueError, match="alphanumeric"):
            slugify("hello world", separator="ab")
        with pytest.raises(ValueError, match="alphanumeric"):
            slugify("hello world", separator="x")

    def test_ss_transliteration_auto(self) -> None:
        assert slugify("Straße", lang="auto") == "strasse"

    def test_oe_transliteration_auto(self) -> None:
        assert slugify("Cœur", lang="auto") == "coeur"

    def test_ae_transliteration_auto(self) -> None:
        assert slugify("Ælfred", lang="auto") == "aelfred"

    # --- Regression tests for bug fixes ---

    def test_backslash_separator_no_crash(self) -> None:
        """Regression: backslash separator must not crash re.sub."""
        assert slugify("hello world", separator="\\") == "hello\\world"

    def test_backslash_separator_collapse(self) -> None:
        """Regression: backslash separator collapse must work."""
        assert slugify("hello   world", separator="\\") == "hello\\world"

    def test_camel_idempotency(self) -> None:
        """Regression: camel style must be idempotent."""
        for text in ["hello world", "HELLO WORLD", "hello 123 world", "Hello World Foo"]:
            result = slugify(text, style="camel")
            assert slugify(result, style="camel") == result, (
                f"camel not idempotent for {text!r} -> {result!r}"
            )

    def test_pascal_idempotency(self) -> None:
        """Regression: pascal style must be idempotent."""
        for text in ["hello world", "HELLO WORLD", "hello 123 world", "Hello World Foo"]:
            result = slugify(text, style="pascal")
            assert slugify(result, style="pascal") == result, (
                f"pascal not idempotent for {text!r} -> {result!r}"
            )

    def test_train_idempotency(self) -> None:
        """Regression: train style must be idempotent."""
        for text in ["hello world", "HELLO WORLD", "hello 123 world", "Hello World Foo"]:
            result = slugify(text, style="train")
            assert slugify(result, style="train") == result, (
                f"train not idempotent for {text!r} -> {result!r}"
            )

    def test_mixed_case_idempotency_all_styles(self) -> None:
        """Regression: mixed-case words with consecutive uppercase must be idempotent."""
        for text in [
            "mixedCASEWord",
            "ABCdef",
            "aBC",
            "ABCDef",
            "a B c",
            "5 A B",
            "5 A B C",
            "a b c d e",
            "a b c d e f",
        ]:
            for style in ["camel", "pascal", "train"]:
                result = slugify(text, style=style)
                assert slugify(result, style=style) == result, (
                    f"{style} not idempotent for {text!r} -> {result!r}"
                )

    def test_unicode_caseless_alpha_idempotency(self) -> None:
        """Regression: caseless alpha (CJK) + uppercase boundary must be idempotent."""
        for text in ["u7WIïこ C", "helloこWorld", "こWorld", "abc你好World"]:
            for style in ["camel", "pascal", "train"]:
                result = slugify(text, style=style, allow_unicode=True)
                assert slugify(result, style=style, allow_unicode=True) == result, (
                    f"{style} not idempotent for {text!r} -> {result!r}"
                )

    def test_camel_idempotency_custom_separator(self) -> None:
        """Regression: camel idempotency with custom separator."""
        result = slugify("hello world", style="camel", separator="_")
        assert slugify(result, style="camel", separator="_") == result

    def test_pascal_idempotency_custom_separator(self) -> None:
        """Regression: pascal idempotency with custom separator."""
        result = slugify("hello world", style="pascal", separator="_")
        assert slugify(result, style="pascal", separator="_") == result

    def test_replacement_non_string_value_raises(self) -> None:
        """Regression: non-string replacement values must raise TypeError."""
        with pytest.raises(TypeError, match="must be strings"):
            slugify("hello", replacements={"h": 123})  # type: ignore[dict-item]
        with pytest.raises(TypeError, match="must be strings"):
            slugify("hello", replacements={"h": None})  # type: ignore[dict-item]

    def test_replacement_non_string_key_raises(self) -> None:
        """Regression: non-string replacement keys must raise TypeError."""
        with pytest.raises(TypeError, match="must be strings"):
            slugify("hello", replacements={1: "x"})  # type: ignore[dict-item]

    def test_replacement_wrong_tuple_length_raises(self) -> None:
        """Regression: replacement tuples with wrong length must raise TypeError."""
        with pytest.raises(TypeError, match="must be .* tuples"):
            slugify("hello", replacements=[("h",)])  # type: ignore[list-item]
        with pytest.raises(TypeError, match="must be .* tuples"):
            slugify("hello", replacements=[("h", "x", "y")])  # type: ignore[list-item]

    def test_replacement_non_tuple_entry_raises(self) -> None:
        """Regression: non-tuple replacement entries must raise TypeError."""
        with pytest.raises(TypeError, match="must be .* tuples"):
            slugify("hello", replacements=["hx"])  # type: ignore[list-item]

    def test_deconfuse_skipped_with_allow_unicode(self) -> None:
        """Regression: deconfuse must not convert Cyrillic when allow_unicode=True."""
        assert slugify("\u0441afe", allow_unicode=True) == "\u0441afe"

    def test_emoji_text_mode_replaces_emoji(self) -> None:
        """Regression: emoji_mode='text' replaces emoji with text description."""
        assert slugify("Hello\U0001f389World", emoji_mode="text") == "helloparty-popperworld"

    def test_emoji_keep_mode_requires_unicode(self) -> None:
        """Regression: emoji_mode='keep' without allow_unicode raises ValueError."""
        with pytest.raises(ValueError, match="allow_unicode=True"):
            slugify("Hello\U0001f389World", emoji_mode="keep")

    def test_stopwords_with_non_alphanumeric_chars(self) -> None:
        """Regression: stopwords containing non-alphanumeric chars must match."""
        assert slugify("hello-world foo", stopwords=["hello-world"]) == "foo"
        assert slugify("hello_world foo", stopwords=["hello_world"]) == "foo"

    def test_post_replacement_after_lowercase(self) -> None:
        """Regression: post-replacements must run after lowercase to match."""
        assert slugify("HELLO", replacements={"hello": "X"}) == "x"
        assert slugify("AElfred", replacements={"ae": "X"}) == "xlfred"

    def test_replacements_not_double_applied(self) -> None:
        """Regression: replacements must not be applied twice (pre + post)."""
        assert slugify("x", replacements={"x": "xx"}) == "xx"
        assert slugify("a", replacements={"a": "ab"}) == "ab"

    def test_replacements_non_ascii_pre_only(self) -> None:
        """Regression: non-ASCII keys only applied in pre-replacements."""
        assert slugify("\u00c6lfred", replacements={"\u00c6": "AE"}) == "aelfred"

    def test_css_safe_camel_idempotent(self) -> None:
        """Regression: css_safe with camel must be idempotent."""
        r = slugify("123 hello", style="camel", css_safe=True)
        assert r == "s123Hello"
        assert slugify(r, style="camel", css_safe=True) == r

    def test_css_safe_pascal_idempotent(self) -> None:
        """Regression: css_safe with pascal must be idempotent."""
        r = slugify("123 hello", style="pascal", css_safe=True)
        assert r == "S123Hello"
        assert slugify(r, style="pascal", css_safe=True) == r

    def test_css_safe_train_idempotent(self) -> None:
        """Regression: css_safe with train must be idempotent."""
        r = slugify("123 hello", style="train", css_safe=True)
        assert r == "S-123-Hello"
        assert slugify(r, style="train", css_safe=True) == r

    def test_emoji_keep_watches_and_arrows(self) -> None:
        """Regression: emoji in U+2300-23FF and U+2B00-2BFF ranges must be preserved."""
        assert (
            slugify("hello \u231a world", emoji_mode="keep", allow_unicode=True)
            == "hello-\u231a-world"
        )
        assert (
            slugify("hello \u23f0 world", emoji_mode="keep", allow_unicode=True)
            == "hello-\u23f0-world"
        )
        assert (
            slugify("hello \u2b06 world", emoji_mode="keep", allow_unicode=True)
            == "hello-\u2b06-world"
        )

    def test_emoji_strip_watches_and_arrows(self) -> None:
        """Regression: emoji in U+2300-23FF and U+2B00-2BFF ranges must be stripped."""
        assert slugify("hello \u231a world", emoji_mode="strip") == "hello-world"
        assert slugify("hello \u23f0 world", emoji_mode="strip") == "hello-world"
        assert slugify("hello \u2b06 world", emoji_mode="strip") == "hello-world"

    def test_deconfuse_missing_cyrillic_homoglyphs(self) -> None:
        """Regression: Cyrillic homoglyphs в, к, м, н, т must be deconfused."""
        assert slugify("\u0432") == "b"  # в -> B -> b
        assert slugify("\u043a") == "k"  # к -> K -> k
        assert slugify("\u043c") == "m"  # м -> M -> m
        assert slugify("\u043d") == "h"  # н -> H -> h
        assert slugify("\u0442") == "t"  # т -> T -> t
        assert slugify("hello \u0432 world") == "hello-b-world"

    def test_camel_consecutive_uppercase_idempotent(self) -> None:
        """Regression: camel with consecutive uppercase letters must be idempotent."""
        r = slugify("a b c", style="camel")
        assert r == "aBC"
        assert slugify(r, style="camel") == r

    def test_pascal_consecutive_uppercase_idempotent(self) -> None:
        """Regression: pascal with consecutive uppercase letters must be idempotent."""
        r = slugify("a b c", style="pascal")
        assert r == "Abc"
        assert slugify(r, style="pascal") == r

    def test_train_consecutive_uppercase_idempotent(self) -> None:
        """Regression: train with consecutive uppercase letters must be idempotent."""
        r = slugify("a b c", style="train")
        assert r == "A-B-C"
        assert slugify(r, style="train") == r

    def test_case_style_normalizes_uppercase_words(self) -> None:
        """Regression: case styles must normalize uppercase words, not preserve them."""
        assert slugify("HELLO WORLD", style="camel") == "helloWorld"
        assert slugify("HELLO WORLD", style="pascal") == "HelloWorld"
        assert slugify("HELLO WORLD", style="train") == "Hello-World"
        assert slugify("CAFÉ NAÏVE", allow_unicode=True, style="camel") == "caféNaïve"
        assert slugify("CAFÉ NAÏVE", allow_unicode=True, style="pascal") == "CaféNaïve"

    def test_camel_digit_lowercase_idempotent(self) -> None:
        """Regression: camel with digit-to-lowercase boundary must be idempotent."""
        r = slugify("123abc def", style="camel")
        assert r == "123abcDef"
        assert slugify(r, style="camel") == r

    def test_non_ascii_stopword_transliterated(self) -> None:
        """Regression: non-ASCII stopwords must be transliterated to match text."""
        assert slugify("caf\u00e9 hello", stopwords=["caf\u00e9"]) == "hello"
        assert slugify("\u00e4 hello", stopwords=["\u00e4"], lang="de") == "hello"

    def test_stopword_auto_lang_german(self) -> None:
        """Regression: stopwords with lang='auto' must use auto-detected language table.

        German ä transliterates to 'ae' via the de table, but NFKD alone
        produces 'a'. The stopword must be normalized with the same table.
        """
        assert slugify("\u00e4 hello", stopwords=["\u00e4"]) == "hello"
        assert slugify("\u00f6 hello", stopwords=["\u00f6"]) == "hello"
        assert slugify("\u00fc hello", stopwords=["\u00fc"]) == "hello"

    def test_css_safe_max_length_idempotent(self) -> None:
        """Regression: css_safe with max_length must be idempotent."""
        r = slugify("123 hello world foo", css_safe=True, max_length=10)
        assert slugify(r, css_safe=True, max_length=10) == r

    def test_train_max_length_idempotent(self) -> None:
        """Regression: train style with max_length must be idempotent."""
        r = slugify("QVbkk1SmU hello world", style="train", max_length=10)
        assert slugify(r, style="train", max_length=10) == r

    def test_underscore_uppercase_camel_idempotent(self) -> None:
        """Regression: _Ksjo with allow_unicode and camel must be idempotent."""
        r = slugify(
            "_#Ksjo",
            allow_unicode=True,
            style="camel",
            css_safe=True,
            max_length=15,
            word_boundary=True,
        )
        assert (
            slugify(
                r,
                allow_unicode=True,
                style="camel",
                css_safe=True,
                max_length=15,
                word_boundary=True,
            )
            == r
        )


class TestCaseStyleIntegration:
    def test_camel(self) -> None:
        assert slugify("hello world foo", style="camel") == "helloWorldFoo"

    def test_pascal(self) -> None:
        assert slugify("hello world foo", style="pascal") == "HelloWorldFoo"

    def test_train(self) -> None:
        assert slugify("hello world foo", style="train") == "Hello-World-Foo"

    def test_dot(self) -> None:
        assert slugify("hello world foo", style="dot") == "hello.world.foo"

    def test_snake(self) -> None:
        assert slugify("hello world foo", style="snake") == "hello_world_foo"

    def test_kebab(self) -> None:
        assert slugify("hello world foo", style="kebab") == "hello-world-foo"

    def test_filename(self) -> None:
        assert slugify("Hello World Foo", style="filename") == "Hello-World-Foo"

    def test_camel_with_unicode(self) -> None:
        assert slugify("España und Übung", style="camel") == "espanaUndUbung"

    def test_css_safe_with_styles(self) -> None:
        """css_safe prefix must adapt to each style preset's separator and case."""
        assert slugify("123 hello", css_safe=True, style="dot") == "s.123.hello"
        assert slugify("123 hello", css_safe=True, style="snake") == "s_123_hello"
        assert slugify("123 hello", css_safe=True, style="kebab") == "s-123-hello"
        assert slugify("123 Hello", css_safe=True, style="filename") == "s-123-Hello"
        assert slugify("123 hello", css_safe=True, style="url") == "s-123-hello"
        assert slugify("123 hello", css_safe=True, style="camel") == "s123Hello"
        assert slugify("123 hello", css_safe=True, style="pascal") == "S123Hello"
        assert slugify("123 hello", css_safe=True, style="train") == "S-123-Hello"


class TestUnicodeCombiningMarks:
    def test_devanagari_combining_marks_preserved(self) -> None:
        """Regression: Devanagari combining vowel signs must not be replaced with separator."""
        assert slugify("नमस्ते", allow_unicode=True) == "नमस्ते"

    def test_arabic_combining_marks_preserved(self) -> None:
        """Regression: Arabic diacritical marks must not be replaced with separator."""
        assert slugify("مَرْحَبَا", allow_unicode=True) == "مَرْحَبَا"

    def test_hebrew_combining_marks_preserved(self) -> None:
        """Regression: Hebrew vowel points must not be replaced with separator."""
        assert slugify("שָׁלוֹם", allow_unicode=True) == "שָׁלוֹם"

    def test_combining_marks_with_separator(self) -> None:
        """Regression: combining marks must stay attached to their base character."""
        assert slugify("नमस्ते world", allow_unicode=True) == "नमस्ते-world"

    def test_combining_marks_idempotent(self) -> None:
        """Regression: slugs with combining marks must be idempotent."""
        r = slugify("नमस्ते world", allow_unicode=True)
        assert slugify(r, allow_unicode=True) == r
