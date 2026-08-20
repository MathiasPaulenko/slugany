from __future__ import annotations

import html
import re
import unicodedata
from collections.abc import Callable

from slugany._config import SlugConfig
from slugany._tables import _CONFUSABLES, _DEFAULT_TABLE, _LANGUAGE_TABLES, _PUNCTUATION_TABLE


def _normalize_punctuation(text: str, config: SlugConfig) -> str:
    if not config.smart_punctuation:
        return text
    text = text.translate(_PUNCTUATION_TABLE)
    if config.emoji_mode != "keep":
        text = text.replace("\u200d", "")
    return text


def _html_entities_decode(text: str, config: SlugConfig) -> str:
    if not config.html_entities:
        return text
    return html.unescape(text)


def _make_replacement_func(replacement: str) -> Callable[[re.Match[str]], str]:
    def _replace(_m: re.Match[str]) -> str:
        return replacement

    return _replace


def _apply_replacements_pre(text: str, config: SlugConfig) -> str:
    for old, new in config.replacements:
        if not old.isascii():
            if config.lowercase:
                text = re.sub(
                    re.escape(old),
                    _make_replacement_func(new),
                    text,
                    flags=re.IGNORECASE,
                )
            else:
                text = text.replace(old, new)
    return text


_EMOJI_RE = re.compile(
    "([\U0001f600-\U0001f64f\U0001f300-\U0001f5ff\U0001f680-\U0001f6ff"
    "\U0001f1e0-\U0001f1ff\U00002700-\U000027bf\U0001f900-\U0001f9ff"
    "\U00002600-\U000026ff\U0001fa00-\U0001fa6f\U0001fa70-\U0001faff"
    "\U0001f000-\U0001f0ff\U00002300-\U000023ff\U00002b00-\U00002bff"
    "\u00a9\u00ae\u203c\u2049\u2122\u2139\u2194-\u2199\u21a9\u21aa\u24c2"
    "\u25aa\u25ab\u25b6\u25c0\u25fb-\u25fe"
    "\u200d\ufe0f]+)",
)


def _handle_emoji(text: str, config: SlugConfig) -> str:
    if config.emoji_mode == "strip":
        return _EMOJI_RE.sub("", text)
    if config.emoji_mode == "text":
        from slugany._tables import _EMOJI_TEXT

        def _replace(m: re.Match[str]) -> str:
            return " ".join(_EMOJI_TEXT.get(ord(c), "") for c in m.group(0)).strip()

        return _EMOJI_RE.sub(_replace, text)
    if config.emoji_mode == "keep":
        if not config.allow_unicode:
            msg = "emoji_mode='keep' requires allow_unicode=True"
            raise ValueError(msg)
        return text
    return text


def _deconfuse(text: str, config: SlugConfig) -> str:
    if config.allow_unicode:
        return text
    return text.translate(_CONFUSABLES)


def _transliterate(text: str, config: SlugConfig) -> str:
    if config.allow_unicode:
        return text

    lang = config.lang
    if lang == "auto":
        lang = _detect_language(text) or ""

    def _transliterate_segment(segment: str) -> str:
        segment = segment.translate(_DEFAULT_TABLE)
        table = _LANGUAGE_TABLES.get(lang)
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
            if config.lowercase:
                new = new.lower()
                text = re.sub(
                    re.escape(old),
                    _make_replacement_func(new),
                    text,
                    flags=re.IGNORECASE,
                )
            else:
                text = text.replace(old, new)
    return text


_ASCII_ALNUM_RE = re.compile(r"[^a-zA-Z0-9]+")


def _is_unicode_word_char(c: str) -> bool:
    """Check if a character is a word character (letter, digit, underscore) or a combining mark."""
    return c.isalnum() or c == "_" or unicodedata.category(c).startswith("M")


def _replace_non_word_unicode(text: str, sep: str) -> str:
    """Replace non-word characters with separator, preserving Unicode combining marks."""
    result: list[str] = []
    for c in text:
        if _is_unicode_word_char(c):
            result.append(c)
        else:
            result.append(sep)
    return "".join(result)


def _lowercase(text: str, config: SlugConfig) -> str:
    return text.lower() if config.lowercase else text


def _remove_stopwords(text: str, config: SlugConfig) -> str:
    if not config.stopwords:
        return text

    def _strip_non_word(sw: str) -> str:
        if config.allow_unicode:
            return "".join(c for c in sw if _is_unicode_word_char(c))
        return _ASCII_ALNUM_RE.sub("", sw)

    def _normalize_stopword(sw: str) -> str:
        if not config.allow_unicode:
            sw = sw.translate(_CONFUSABLES)
            sw = sw.translate(_DEFAULT_TABLE)
            lang = config.lang
            if lang == "auto":
                lang = _detect_language(sw) or ""
            table = _LANGUAGE_TABLES.get(lang)
            if table:
                sw = sw.translate(table)
            sw = unicodedata.normalize("NFKD", sw).encode("ascii", "ignore").decode("ascii")
        return _strip_non_word(sw).lower()

    lower_sw = {_normalize_stopword(sw) for sw in config.stopwords}
    return " ".join(w for w in text.split() if _strip_non_word(w).lower() not in lower_sw)


def _replace_non_alphanumeric(text: str, config: SlugConfig) -> str:
    sep = config.separator
    if config.allow_unicode:
        if config.emoji_mode in ("keep", "text"):
            parts = _EMOJI_RE.split(text)
            processed = [
                _replace_non_word_unicode(part, sep) if i % 2 == 0 else part
                for i, part in enumerate(parts)
            ]
            return sep.join(processed)
        return _replace_non_word_unicode(text, sep)
    if config.emoji_mode in ("keep", "text"):
        parts = _EMOJI_RE.split(text)
        processed = [
            _ASCII_ALNUM_RE.sub(lambda _m: sep, part) if i % 2 == 0 else part
            for i, part in enumerate(parts)
        ]
        return sep.join(processed)
    return _ASCII_ALNUM_RE.sub(lambda _m: sep, text)


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
        if text[config.max_length :].startswith(config.separator):
            return truncated
        stripped = False
        for i in range(len(config.separator) - 1, 0, -1):
            if truncated.endswith(config.separator[:i]):
                truncated = truncated[:-i]
                stripped = True
                break
        if stripped:
            return truncated
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
            or (prev.isalpha() and not prev.isupper() and char.isupper())
            or (prev.isupper() and char.isupper())
            or (prev.isdigit() and char.isupper())
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
    raw_words = [w for w in text.split(sep) if w]
    if not raw_words:
        return ""
    if config.style in ("camel", "pascal", "train"):

        def _capitalize(w: str) -> str:
            alpha_chars = [c for c in w if c.isalpha()]
            if not alpha_chars:
                return w
            return w[0].upper() + w[1:]

        def _normalize_upper(w: str) -> str:
            if not w or not w[0].isalpha():
                return w
            if not all(c.isalpha() for c in w):
                return w
            if len(w) <= 3:
                return w
            if all(c.isupper() for c in w):
                return w[0] + w[1:].lower()
            return w

        words: list[str] = []
        for w in raw_words:
            w = _normalize_upper(w)
            has_upper = any(c.isupper() for c in w)
            has_lower = any(c.islower() for c in w)
            has_caseless = any(c.isalpha() and not c.isupper() and not c.islower() for c in w)
            if has_upper and (has_lower or has_caseless):
                parts = _split_case_boundaries(w)
                if config.style == "pascal":
                    cap = "".join(_capitalize(p) for p in parts)
                    cap = _normalize_upper(cap)
                    words.append(cap)
                else:
                    words.extend(parts)
            else:
                words.append(w)
        if config.style == "pascal":
            merged_words: list[str] = []
            for w in words:
                if (
                    merged_words
                    and len(w) == 1
                    and w.isalpha()
                    and merged_words[-1].isalpha()
                    and all(not c.isupper() for c in merged_words[-1])
                ):
                    merged_words[-1] += w
                else:
                    merged_words.append(w)
            words = merged_words
    else:
        words = raw_words

    if config.style == "camel":
        first = words[0]
        if first and first[0].isalpha():
            first_chars = list(first)
            for i, c in enumerate(first_chars):
                if c.isalpha():
                    first_chars[i] = c.lower()
                    break
            first = "".join(first_chars)
        rest = "".join(_capitalize(w) for w in words[1:])
        rest_alpha = [c for c in rest if c.isalpha()]
        rest_all_single = all(len(w) == 1 for w in words[1:] if w)
        if (
            len(rest_alpha) > 4
            and all(c.isupper() for c in rest_alpha)
            and all(c.isalpha() for c in rest)
            and rest_all_single
        ):
            rest = rest[0] + rest[1:].lower()
        return first + rest
    if config.style == "pascal":
        return "".join(_capitalize(w) for w in words)
    if config.style == "train":
        return config.separator.join(_capitalize(w) for w in words)
    return text


def _detect_language(text: str) -> str | None:
    from slugany._tables import _LANG_DETECT_RANGES

    counts: dict[str, int] = {}
    for lang, ranges in _LANG_DETECT_RANGES.items():
        count = sum(1 for c in text if any(lo <= ord(c) <= hi for lo, hi in ranges))
        if count > 0:
            counts[lang] = count
    if not counts:
        return None
    return max(counts, key=lambda k: counts[k])


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
