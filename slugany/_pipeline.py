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
    _trim_separators,
    _truncate,
    _apply_fallback,
    _apply_css_safe,
    _apply_case_style,
    _truncate,
    _trim_separators,
]

_POST_FALLBACK_STEPS: list[Callable[[str, SlugConfig], str]] = [
    _deconfuse,
    _transliterate,
    _lowercase,
    _apply_replacements_post,
    _replace_non_alphanumeric,
    _collapse_separators,
    _trim_separators,
    _truncate,
]


def _run_pipeline(text: str, config: SlugConfig) -> str:
    for step in _STEPS:
        if not text and step is not _apply_fallback:
            continue
        was_empty = not text
        text = step(text, config)
        if step is _apply_fallback and was_empty and text:
            for norm_step in _POST_FALLBACK_STEPS:
                text = norm_step(text, config)
    return text
