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
        text = text.replace(old, new)
    return text


_EMOJI_RE = re.compile(
    "[\U0001f600-\U0001f64f\U0001f300-\U0001f5ff\U0001f680-\U0001f6ff"
    "\U0001f1e0-\U0001f1ff\U00002700-\U000027bf\U0001f900-\U0001f9ff"
    "\U00002600-\U000026ff\U0001fa00-\U0001fa6f\U0001fa70-\U0001faff"
    "\U0001f000-\U0001f0ff]+",
    re.UNICODE,
)


def _handle_emoji(text: str, config: SlugConfig) -> str:
    if config.emoji_mode == "strip":
        return _EMOJI_RE.sub("", text)
    return text


def _deconfuse(text: str, config: SlugConfig) -> str:
    return text.translate(_CONFUSABLES)


def _transliterate(text: str, config: SlugConfig) -> str:
    if config.allow_unicode:
        return text
    text = text.translate(_DEFAULT_TABLE)
    table = _LANGUAGE_TABLES.get(config.lang)
    if table:
        text = text.translate(table)
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def _apply_replacements_post(text: str, config: SlugConfig) -> str:
    for old, new in config.replacements:
        text = text.replace(old, new)
    return text


def _lowercase(text: str, config: SlugConfig) -> str:
    return text.lower() if config.lowercase else text


def _remove_stopwords(text: str, config: SlugConfig) -> str:
    if not config.stopwords:
        return text
    lower_sw = {sw.lower() for sw in config.stopwords}
    return " ".join(w for w in text.split() if w.lower() not in lower_sw)


_ASCII_ALNUM_RE = re.compile(r"[^a-zA-Z0-9]+")
_UNICODE_ALNUM_RE = re.compile(r"[^\w]+", re.UNICODE)


def _replace_non_alphanumeric(text: str, config: SlugConfig) -> str:
    pattern = _UNICODE_ALNUM_RE if config.allow_unicode else _ASCII_ALNUM_RE
    return pattern.sub(config.separator, text)


def _collapse_separators(text: str, config: SlugConfig) -> str:
    if not config.separator:
        return text
    sep = re.escape(config.separator)
    return re.sub(f"{sep}+", config.separator, text)


def _trim_separators(text: str, config: SlugConfig) -> str:
    if not config.separator:
        return text
    sep = re.escape(config.separator)
    text = re.sub(f"^{sep}+|{sep}+$", "", text)
    sep_str = config.separator
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


def _apply_case_style(text: str, config: SlugConfig) -> str:
    if not config.style:
        return text
    sep = config.separator if config.separator else "-"
    words = [w for w in text.split(sep) if w]
    if not words:
        return ""
    if config.style == "camel":
        return words[0].lower() + "".join(w.capitalize() for w in words[1:])
    if config.style == "pascal":
        return "".join(w.capitalize() for w in words)
    if config.style == "train":
        return config.separator.join(w.capitalize() for w in words)
    return text


def _apply_fallback(text: str, config: SlugConfig) -> str:
    if not text and config.fallback:
        return config.fallback
    return text


def _apply_css_safe(text: str, config: SlugConfig) -> str:
    if config.css_safe and text and text[0].isdigit():
        return f"s{config.separator}{text}"
    return text
