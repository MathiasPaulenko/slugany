from __future__ import annotations

from collections.abc import Iterable, Mapping
from functools import lru_cache

from slugany._config import SlugConfig
from slugany._pipeline import _run_pipeline


@lru_cache(maxsize=512)
def _slugify_cached(text: str, config: SlugConfig) -> str:
    return _run_pipeline(text, config)


def slugify(
    text: str,
    *,
    separator: str | None = None,
    lowercase: bool | None = None,
    max_length: int = 0,
    word_boundary: bool = False,
    stopwords: Iterable[str] | None = None,
    allow_unicode: bool = False,
    replacements: Mapping[str, str] | Iterable[tuple[str, str]] | None = None,
    style: str | None = None,
    lang: str = "auto",
    fallback: str = "",
    emoji_mode: str = "strip",
    css_safe: bool = False,
    html_entities: bool = True,
    smart_punctuation: bool = True,
) -> str:
    """Convert text into a URL-friendly slug.

    Args:
        text: The text to slugify. Must be a string.
        separator: Separator between words. Defaults to ``"-"`` (or the
            style preset's separator when a style is specified).
        lowercase: Whether to lowercase the output. Defaults to ``True``
            (or the style preset's setting when a style is specified).
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
            empty ``separator``, or empty replacement key is provided.
    """
    if not isinstance(text, str):
        msg = f"text must be a string, got {type(text).__name__}"
        raise TypeError(msg)
    config = SlugConfig.from_kwargs(
        separator=separator,
        lowercase=lowercase,
        max_length=max_length,
        word_boundary=word_boundary,
        stopwords=stopwords,
        allow_unicode=allow_unicode,
        replacements=replacements,
        style=style,
        lang=lang,
        fallback=fallback,
        emoji_mode=emoji_mode,
        css_safe=css_safe,
        html_entities=html_entities,
        smart_punctuation=smart_punctuation,
    )
    return _slugify_cached(text, config)


slugify.cache_info = _slugify_cached.cache_info  # type: ignore[attr-defined]
slugify.cache_clear = _slugify_cached.cache_clear  # type: ignore[attr-defined]


def slugify_batch(
    texts: Iterable[str],
    *,
    separator: str | None = None,
    lowercase: bool | None = None,
    max_length: int = 0,
    word_boundary: bool = False,
    stopwords: Iterable[str] | None = None,
    allow_unicode: bool = False,
    replacements: Mapping[str, str] | Iterable[tuple[str, str]] | None = None,
    style: str | None = None,
    lang: str = "auto",
    fallback: str = "",
    emoji_mode: str = "strip",
    css_safe: bool = False,
    html_entities: bool = True,
    smart_punctuation: bool = True,
) -> list[str]:
    """Slugify multiple texts in a single call.

    Args:
        texts: Iterable of strings to slugify.
        separator: Separator between words. Defaults to ``"-"`` (or the
            style preset's separator when a style is specified).
        lowercase: Whether to lowercase the output. Defaults to ``True``
            (or the style preset's setting when a style is specified).
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
        A list of slugified strings, one per input text.

    Raises:
        TypeError: If any text is not a string.
        ValueError: If an invalid ``style``, ``lang``, ``emoji_mode``,
            empty ``separator``, or empty replacement key is provided.
    """
    return [
        slugify(
            text,
            separator=separator,
            lowercase=lowercase,
            max_length=max_length,
            word_boundary=word_boundary,
            stopwords=stopwords,
            allow_unicode=allow_unicode,
            replacements=replacements,
            style=style,
            lang=lang,
            fallback=fallback,
            emoji_mode=emoji_mode,
            css_safe=css_safe,
            html_entities=html_entities,
            smart_punctuation=smart_punctuation,
        )
        for text in texts
    ]
