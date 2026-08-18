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
    """Convert text into a URL-friendly slug.

    Args:
        text: The text to slugify. Must be a string.
        separator: Separator between words. Defaults to ``"-"``.
        lowercase: Whether to lowercase the output. Defaults to ``True``.
        max_length: Maximum slug length. ``0`` means no limit.
        word_boundary: Truncate at the last word boundary within ``max_length``.
        stopwords: Iterable of words to remove from the output.
        allow_unicode: Preserve Unicode characters instead of transliterating.
        replacements: Mapping or iterable of ``(old, new)`` pairs applied pre and post.
        style: Case style preset (``kebab``, ``snake``, ``camel``,
            ``pascal``, ``dot``, ``train``, ``filename``, ``url``).
        lang: Language for transliteration
            (``auto``, ``es``, ``pt``, ``de``, ``fr``, ``it``).
        fallback: String to return when the slug would be empty.
            This value is returned as-is — it should be a valid slug.
        emoji_mode: How to handle emojis (``strip``, ``text``, ``keep``).
        css_safe: Prefix with ``s{separator}`` if the slug starts with a digit.
        html_entities: Decode HTML entities like ``&amp;``.
        smart_punctuation: Normalize smart quotes, dashes, and zero-width
            characters.

    Returns:
        The slugified string.

    Raises:
        TypeError: If ``text`` is not a string.
        ValueError: If an invalid ``style``, ``lang``, ``emoji_mode``,
            or empty ``separator`` is provided.
    """
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
    """Slugify multiple texts in a single call.

    Args:
        texts: Iterable of strings to slugify.
        **kwargs: Additional keyword arguments passed to :func:`slugify`.

    Returns:
        A list of slugified strings, one per input text.
    """
    return [slugify(text, **kwargs) for text in texts]
