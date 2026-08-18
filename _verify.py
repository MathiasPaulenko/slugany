from slugany._tables import (
    _PUNCTUATION_TABLE,
    _ES_TABLE,
    _PT_TABLE,
    _DE_TABLE,
    _LANGUAGE_TABLES,
    _CONFUSABLES,
)
from slugany._config import SlugConfig, _STYLE_PRESETS

assert "Bob\u2019s".translate(_PUNCTUATION_TABLE) == "Bob's"
assert "a\u2014b".translate(_PUNCTUATION_TABLE) == "a-b"
assert "a\u00a0b".translate(_PUNCTUATION_TABLE) == "a b"
assert "a\u200bb".translate(_PUNCTUATION_TABLE) == "ab"
assert "Espa\u00f1a".translate(_ES_TABLE) == "Espana"
assert "Cora\u00e7\u00e3o".translate(_PT_TABLE) == "Coracao"
assert "\u00dcbung".translate(_DE_TABLE) == "Uebung"
assert "es" in _LANGUAGE_TABLES
assert "pt" in _LANGUAGE_TABLES
assert "de" in _LANGUAGE_TABLES
assert "fr" in _LANGUAGE_TABLES
assert "it" in _LANGUAGE_TABLES
assert "\u0441afe".translate(_CONFUSABLES) == "cafe"

c = SlugConfig()
assert c.separator == "-"
assert c.lowercase is True
assert c.max_length == 0
assert c.word_boundary is False
assert c.stopwords == frozenset()
assert c.allow_unicode is False
assert c.replacements == frozenset()
assert c.style is None
assert c.lang == "auto"
assert c.fallback == ""
assert c.emoji_mode == "strip"
assert c.css_safe is False
assert c.html_entities is True
assert c.smart_punctuation is True

c2 = SlugConfig(separator="_")
assert c2.separator == "_"
assert "url" in _STYLE_PRESETS
assert "filename" in _STYLE_PRESETS
assert "kebab" in _STYLE_PRESETS
assert "snake" in _STYLE_PRESETS
assert "camel" in _STYLE_PRESETS
assert "pascal" in _STYLE_PRESETS
assert "dot" in _STYLE_PRESETS
assert "train" in _STYLE_PRESETS

c3 = SlugConfig.from_kwargs(style="url", separator="_")
assert c3.separator == "_"
c4 = SlugConfig.from_kwargs(style="filename")
assert c4.lowercase is False

from slugany._steps import _normalize_punctuation, _html_entities_decode, _apply_replacements_pre, _handle_emoji, _deconfuse, _transliterate, _apply_replacements_post, _lowercase, _remove_stopwords, _replace_non_alphanumeric, _collapse_separators, _trim_separators, _truncate, _apply_case_style, _apply_fallback

assert _normalize_punctuation("Bob's caf\u00e9", SlugConfig()) == "Bob's caf\u00e9"
assert _html_entities_decode("Bob&amp;Caf\u00e9", SlugConfig()) == "Bob&Caf\u00e9"
assert _apply_replacements_pre("Hello", SlugConfig.from_kwargs(replacements={"ll": "2"})) == "He2o"
assert _handle_emoji("Hello \U0001F389 World", SlugConfig()) == "Hello  World"
assert _deconfuse("\u0441afe", SlugConfig()) == "cafe"
assert _transliterate("Espa\u00f1a", SlugConfig(lang="es")) == "Espana"
assert _transliterate("\u00dcbung", SlugConfig(lang="de")) == "Uebung"
assert _apply_replacements_post("hello", SlugConfig.from_kwargs(replacements={"ll": "2"})) == "he2o"
assert _lowercase("Hello", SlugConfig()) == "hello"
assert _remove_stopwords("the hello world", SlugConfig(stopwords=frozenset({"the"}))) == "hello world"
assert _replace_non_alphanumeric("Hello World!!!", SlugConfig()) == "Hello-World-"
assert _collapse_separators("a---b", SlugConfig()) == "a-b"
assert _trim_separators("-hello-world-", SlugConfig()) == "hello-world"
assert _truncate("hello-world-foo", SlugConfig(max_length=10)) == "hello-worl"
assert _truncate("hello-world-foo", SlugConfig(max_length=10, word_boundary=True)) == "hello"
assert _apply_case_style("hello-world", SlugConfig.from_kwargs(style="camel")) == "helloWorld"
assert _apply_fallback("", SlugConfig(fallback="untitled")) == "untitled"

from slugany._pipeline import _run_pipeline

assert _run_pipeline("\u00a1Hola Mundo!", SlugConfig()) == "hola-mundo"
assert _run_pipeline("Caf\u00e9 r\u00e9sum\u00e9", SlugConfig()) == "cafe-resume"

from slugany._slugify import _slugify_cached, slugify, slugify_batch

assert _slugify_cached("Hola", SlugConfig()) == "hola"
assert slugify("\u00a1Hola Mundo!") == "hola-mundo"
assert slugify.cache_info() is not None
assert slugify_batch(["Hello World", "Caf\u00e9"]) == ["hello-world", "cafe"]

from slugany._validator import is_slug

assert is_slug("hello-world") is True
assert is_slug("hello world") is False
assert is_slug("") is False
print("OK")
