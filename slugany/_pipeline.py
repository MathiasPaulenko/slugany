from __future__ import annotations

from collections.abc import Callable

from slugany._config import SlugConfig
from slugany._steps import (
    _apply_case_style,
    _apply_css_safe,
    _apply_fallback,
    _apply_replacements_post,
    _apply_replacements_pre,
    _collapse_separators,
    _deconfuse,
    _handle_emoji,
    _html_entities_decode,
    _lowercase,
    _normalize_punctuation,
    _remove_stopwords,
    _replace_non_alphanumeric,
    _transliterate,
    _trim_separators,
    _truncate,
)

_STEPS: list[Callable[[str, SlugConfig], str]] = [
    _html_entities_decode,
    _normalize_punctuation,
    _apply_replacements_pre,
    _handle_emoji,
    _deconfuse,
    _transliterate,
    _lowercase,
    _apply_replacements_post,
    _remove_stopwords,
    _replace_non_alphanumeric,
    _collapse_separators,
    _truncate,
    _trim_separators,
    _apply_fallback,
    _apply_css_safe,
    _apply_case_style,
    _truncate,
    _trim_separators,
]


def _run_pipeline(text: str, config: SlugConfig) -> str:
    for step in _STEPS:
        if not text and step is not _apply_fallback:
            continue
        text = step(text, config)
    return text
