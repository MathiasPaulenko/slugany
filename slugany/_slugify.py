from __future__ import annotations

from collections.abc import Iterable, Mapping
from functools import lru_cache
from typing import Any

from slugany._config import SlugConfig
from slugany._pipeline import _run_pipeline

_SENTINEL: Any = object()


@lru_cache(maxsize=512)
def _slugify_cached(text: str, config: SlugConfig) -> str:
    return _run_pipeline(text, config)


def slugify(
    text: str,
    *,
    separator: Any = _SENTINEL,
    lowercase: Any = _SENTINEL,
    max_length: Any = _SENTINEL,
    word_boundary: Any = _SENTINEL,
    stopwords: Iterable[str] | None = None,
    allow_unicode: Any = _SENTINEL,
    replacements: Mapping[str, str] | Iterable[tuple[str, str]] | None = None,
    style: str | None = None,
    lang: Any = _SENTINEL,
    fallback: Any = _SENTINEL,
    emoji_mode: Any = _SENTINEL,
    css_safe: Any = _SENTINEL,
    html_entities: Any = _SENTINEL,
    smart_punctuation: Any = _SENTINEL,
) -> str:
    if not isinstance(text, str):
        msg = f"text must be a string, got {type(text).__name__}"
        raise TypeError(msg)
    kwargs: dict[str, Any] = {}
    if separator is not _SENTINEL:
        kwargs["separator"] = separator
    if lowercase is not _SENTINEL:
        kwargs["lowercase"] = lowercase
    if max_length is not _SENTINEL:
        kwargs["max_length"] = max_length
    if word_boundary is not _SENTINEL:
        kwargs["word_boundary"] = word_boundary
    if allow_unicode is not _SENTINEL:
        kwargs["allow_unicode"] = allow_unicode
    if style is not _SENTINEL:
        kwargs["style"] = style
    if lang is not _SENTINEL:
        kwargs["lang"] = lang
    if fallback is not _SENTINEL:
        kwargs["fallback"] = fallback
    if emoji_mode is not _SENTINEL:
        kwargs["emoji_mode"] = emoji_mode
    if css_safe is not _SENTINEL:
        kwargs["css_safe"] = css_safe
    if html_entities is not _SENTINEL:
        kwargs["html_entities"] = html_entities
    if smart_punctuation is not _SENTINEL:
        kwargs["smart_punctuation"] = smart_punctuation
    if stopwords is not None:
        kwargs["stopwords"] = stopwords
    if replacements is not None:
        kwargs["replacements"] = replacements
    config = SlugConfig.from_kwargs(**kwargs)
    return _slugify_cached(text, config)


slugify.cache_info = _slugify_cached.cache_info  # type: ignore[attr-defined]
slugify.cache_clear = _slugify_cached.cache_clear  # type: ignore[attr-defined]


def slugify_batch(texts: Iterable[str], **kwargs: Any) -> list[str]:
    return [slugify(text, **kwargs) for text in texts]
