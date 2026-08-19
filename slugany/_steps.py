from __future__ import annotations

import html
import re
import unicodedata

from slugany._config import SlugConfig
from slugany._tables import _CONFUSABLES, _DEFAULT_TABLE, _LANGUAGE_TABLES, _PUNCTUATION_TABLE


def _normalize_punctuation(text: str, config: SlugConfig) -> str:
    if not config.smart_punctuation:
        return text
    return text.translate(_PUNCTUATION_TABLE)


def _html_entities_decode(text: str, config: SlugConfig) -> str:
    if not config.html_entities:
        return text
    return html.unescape(text)


def _apply_replacements_pre(text: str, config: SlugConfig) -> str:
    for old, new in config.replacements:
        if not old.isascii():
            text = text.replace(old, new)
    return text


_EMOJI_RE = re.compile(
    "([\U0001f600-\U0001f64f\U0001f300-\U0001f5ff\U0001f680-\U0001f6ff"
    "\U0001f1e0-\U0001f1ff\U00002700-\U000027bf\U0001f900-\U0001f9ff"
    "\U00002600-\U000026ff\U0001fa00-\U0001fa6f\U0001fa70-\U0001faff"
    "\U0001f000-\U0001f0ff\U00002300-\U000023ff\U00002b00-\U00002bff"
    "\u00a9\u00ae\u203c\u2049\u2122\u2139\u2194-\u2199\u21a9\u21aa\u24c2"
    "\u25aa\u25ab\u25b6\u25c0\u25fb-\u25fe]+)",
)


def _handle_emoji(text: str, config: SlugConfig) -> str:
    if config.emoji_mode == "strip":
        return _EMOJI_RE.sub("", text)
    # "text" and "keep" modes preserve emojis as-is
    return text


def _deconfuse(text: str, config: SlugConfig) -> str:
    if config.allow_unicode:
        return text
    return text.translate(_CONFUSABLES)


def _transliterate(text: str, config: SlugConfig) -> str:
    if config.allow_unicode:
        return text

    def _transliterate_segment(segment: str) -> str:
        segment = segment.translate(_DEFAULT_TABLE)
        table = _LANGUAGE_TABLES.get(config.lang)
        if table:
            segment = segment.translate(table)
        segment = unicodedata.normalize("NFKD", segment)
        return segment.encode("ascii", "ignore").decode("ascii")

    if config.emoji_mode in ("keep", "text"):
        parts = _EMOJI_RE.split(text)
        processed = [
            _transliterate_segment(part) if i % 2 == 0 else part for i, part in enumerate(parts)
        ]
        return "".join(processed)

    return _transliterate_segment(text)


def _apply_replacements_post(text: str, config: SlugConfig) -> str:
    for old, new in config.replacements:
        if old.isascii():
            text = text.replace(old, new)
    return text


_ASCII_ALNUM_RE = re.compile(r"[^a-zA-Z0-9]+")
_UNICODE_ALNUM_RE = re.compile(r"[^\w]+")


def _lowercase(text: str, config: SlugConfig) -> str:
    return text.lower() if config.lowercase else text


def _remove_stopwords(text: str, config: SlugConfig) -> str:
    if not config.stopwords:
        return text
    pattern = _UNICODE_ALNUM_RE if config.allow_unicode else _ASCII_ALNUM_RE

    def _normalize_stopword(sw: str) -> str:
        if not config.allow_unicode:
            sw = sw.translate(_CONFUSABLES)
            sw = sw.translate(_DEFAULT_TABLE)
            table = _LANGUAGE_TABLES.get(config.lang)
            if table:
                sw = sw.translate(table)
            sw = unicodedata.normalize("NFKD", sw).encode("ascii", "ignore").decode("ascii")
        return pattern.sub("", sw).lower()

    lower_sw = {_normalize_stopword(sw) for sw in config.stopwords}
    return " ".join(w for w in text.split() if pattern.sub("", w).lower() not in lower_sw)


def _replace_non_alphanumeric(text: str, config: SlugConfig) -> str:
    pattern = _UNICODE_ALNUM_RE if config.allow_unicode else _ASCII_ALNUM_RE
    sep = config.separator
    if config.emoji_mode in ("keep", "text"):
        parts = _EMOJI_RE.split(text)
        processed = [
            pattern.sub(lambda _m: sep, part) if i % 2 == 0 else part
            for i, part in enumerate(parts)
        ]
        return sep.join(processed)
    return pattern.sub(lambda _m: sep, text)


def _collapse_separators(text: str, config: SlugConfig) -> str:
    if not config.separator:
        return text
    sep = re.escape(config.separator)
    return re.sub(f"(?:{sep})+", lambda _m: config.separator, text)


def _trim_separators(text: str, config: SlugConfig) -> str:
    if not config.separator:
        return text
    sep = re.escape(config.separator)
    text = re.sub(f"^(?:{sep})+|(?:{sep})+$", "", text)
    sep_str = config.separator
    if all(not c.isalnum() for c in sep_str):
        for i in range(len(sep_str) - 1, 0, -1):
            if text.startswith(sep_str[:i]):
                text = text[i:]
                break
        for i in range(len(sep_str) - 1, 0, -1):
            if text.endswith(sep_str[-i:]):
                text = text[:-i]
                break
    return text


def _truncate(text: str, config: SlugConfig) -> str:
    if config.max_length <= 0 or len(text) <= config.max_length:
        return text
    if config.word_boundary and config.separator:
        truncated = text[: config.max_length]
        last_sep = truncated.rfind(config.separator)
        if last_sep > 0:
            return truncated[:last_sep]
    return text[: config.max_length]


def _split_case_boundaries(word: str) -> list[str]:
    """Split a single word into sub-words at case boundaries.

    Handles both ASCII and Unicode case transitions, e.g. "caféBistro" ->
    ["café", "Bistro"].
    """
    if not word:
        return []
    result: list[str] = []
    current = word[0]
    for i in range(1, len(word)):
        prev = word[i - 1]
        char = word[i]
        should_split = (
            (prev.islower() and char.isupper())
            or (prev.isupper() and char.isupper() and i + 1 < len(word) and word[i + 1].islower())
            or (prev.isdigit() and char.isupper())
            or (prev.isalpha() and char.isdigit())
            or (not prev.isalpha() and not prev.isdigit() and char.isupper())
        )
        if should_split:
            result.append(current)
            current = char
        else:
            current += char
    if current:
        result.append(current)
    return result


def _apply_case_style(text: str, config: SlugConfig) -> str:
    if not config.style:
        return text
    sep = config.separator if config.separator else "-"
    words = [w for w in text.split(sep) if w]
    if not words:
        return ""
    if len(words) == 1 and config.style in ("camel", "pascal", "train"):
        words = _split_case_boundaries(words[0])
    if config.style == "camel":
        return words[0].lower() + "".join(w[0].upper() + w[1:] for w in words[1:])
    if config.style == "pascal":
        return "".join(w[0].upper() + w[1:] for w in words)
    if config.style == "train":
        return config.separator.join(w[0].upper() + w[1:] for w in words)
    return text


def _apply_fallback(text: str, config: SlugConfig) -> str:
    if not text and config.fallback:
        return config.fallback
    return text


def _apply_css_safe(text: str, config: SlugConfig) -> str:
    if config.css_safe and text and text[0].isdigit():
        if config.style in ("camel", "pascal"):
            prefix = "s" if config.style == "camel" else "S"
            return prefix + text
        if config.style == "train":
            return f"S{config.separator}{text}"
        return f"s{config.separator}{text}"
    return text
