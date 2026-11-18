from __future__ import annotations

import dataclasses
from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Any, cast

_STYLE_PRESETS: dict[str, dict[str, object]] = {
    "url": {"separator": "-", "lowercase": True},
    "filename": {"separator": "-", "lowercase": False},
    "kebab": {"separator": "-", "lowercase": True},
    "snake": {"separator": "_", "lowercase": True},
    "camel": {"separator": "-", "lowercase": False, "style": "camel"},
    "pascal": {"separator": "-", "lowercase": False, "style": "pascal"},
    "dot": {"separator": ".", "lowercase": True},
    "train": {"separator": "-", "lowercase": False, "style": "train"},
}

_VALID_LANGS: frozenset[str] = frozenset({"auto", "es", "pt", "de", "fr", "it"})
_VALID_EMOJI_MODES: frozenset[str] = frozenset({"strip", "text", "keep"})

# Fields where an explicit None means "not provided" and must fall back to
# the default. separator/lowercase have their own None semantics (style
# preset fallback) and style=None means "no style", so they are excluded.
_NONE_MEANS_DEFAULT: tuple[str, ...] = (
    "max_length",
    "word_boundary",
    "allow_unicode",
    "fallback",
    "emoji_mode",
    "css_safe",
    "html_entities",
    "smart_punctuation",
    "lang",
    "stopwords",
    "replacements",
)

_BOOL_FIELDS: tuple[str, ...] = (
    "lowercase",
    "word_boundary",
    "allow_unicode",
    "css_safe",
    "html_entities",
    "smart_punctuation",
)


def _coerce_stopwords(stopwords: Any) -> frozenset[str]:
    if isinstance(stopwords, str):
        msg = (
            "stopwords must be an iterable of strings, got a bare string; "
            "wrap it in a list, e.g. stopwords=['the', 'a']."
        )
        raise TypeError(msg)
    if isinstance(stopwords, Mapping):
        msg = (
            "stopwords must be an iterable of strings, "
            f"got a mapping of type {type(stopwords).__name__}."
        )
        raise TypeError(msg)
    if not isinstance(stopwords, frozenset):
        try:
            stopwords = frozenset(stopwords)
        except TypeError:
            msg = f"stopwords must be an iterable of strings, got {type(stopwords).__name__}."
            raise TypeError(msg) from None
    for sw in stopwords:
        if not isinstance(sw, str):
            msg = f"stopwords entries must be strings, got {type(sw).__name__}."
            raise TypeError(msg)
    return cast("frozenset[str]", stopwords)


def _coerce_replacements(replacements: Any) -> tuple[tuple[str, str], ...]:
    if isinstance(replacements, str):
        msg = (
            "replacements must be a mapping or an ordered iterable of (old, new) "
            "pairs, got a bare string; wrap it in a list, e.g. replacements=[...]."
        )
        raise TypeError(msg)
    if isinstance(replacements, Mapping):
        replacements = tuple(replacements.items())
    elif isinstance(replacements, (set, frozenset)):
        msg = (
            "replacements must be a mapping or an ordered iterable of (old, new) "
            f"pairs, got {type(replacements).__name__}; sets are not allowed "
            "because their iteration order is not deterministic."
        )
        raise TypeError(msg)
    elif not isinstance(replacements, tuple):
        try:
            replacements = tuple(replacements)
        except TypeError:
            msg = (
                "replacements must be a mapping or an iterable of (old, new) pairs, "
                f"got {type(replacements).__name__}."
            )
            raise TypeError(msg) from None
    for pair in replacements:
        if not isinstance(pair, tuple) or len(pair) != 2:
            msg = f"replacements entries must be (str, str) tuples, got {pair!r}."
            raise TypeError(msg)
        old, new = pair
        if not isinstance(old, str) or not isinstance(new, str):
            msg = f"replacements keys and values must be strings, got {pair!r}."
            raise TypeError(msg)
        if not old:
            msg = "replacements keys must be non-empty strings."
            raise ValueError(msg)
    return cast("tuple[tuple[str, str], ...]", replacements)


@dataclass(frozen=True, slots=True)
class SlugConfig:
    """Immutable configuration for the slugify pipeline.

    All fields have sensible defaults and are validated on construction,
    both via :meth:`from_kwargs` and direct instantiation. Use
    :meth:`from_kwargs` to create a config from keyword arguments with
    style preset merging.

    Passing ``None`` for any field via :meth:`from_kwargs` means "not
    provided" and falls back to the default (or the style preset's value
    for ``separator``/``lowercase``). Direct instantiation requires
    concrete values; an empty ``separator`` is allowed there for advanced
    use (it disables separator handling).
    """

    separator: str = "-"
    lowercase: bool = True
    max_length: int = 0
    word_boundary: bool = False
    stopwords: frozenset[str] = field(default_factory=frozenset)
    allow_unicode: bool = False
    replacements: tuple[tuple[str, str], ...] = field(default_factory=tuple)
    style: str | None = None
    lang: str = "auto"
    fallback: str = ""
    emoji_mode: str = "strip"
    css_safe: bool = False
    html_entities: bool = True
    smart_punctuation: bool = True

    def __post_init__(self) -> None:
        separator = self.separator
        if not isinstance(separator, str):
            msg = f"separator must be a string, got {type(separator).__name__}."
            raise TypeError(msg)
        if any(c.isalnum() for c in separator):
            msg = f"separator must not contain alphanumeric characters, got {separator!r}."
            raise ValueError(msg)
        if any(c.isspace() for c in separator):
            msg = "separator must not contain whitespace."
            raise ValueError(msg)

        for name in _BOOL_FIELDS:
            value = getattr(self, name)
            if not isinstance(value, bool):
                msg = f"{name} must be a boolean, got {type(value).__name__}."
                raise TypeError(msg)

        max_length = self.max_length
        if not isinstance(max_length, int) or isinstance(max_length, bool):
            msg = f"max_length must be an integer, got {type(max_length).__name__}."
            raise TypeError(msg)
        if max_length < 0:
            msg = f"max_length must be non-negative, got {max_length}."
            raise ValueError(msg)

        if not isinstance(self.fallback, str):
            msg = f"fallback must be a string, got {type(self.fallback).__name__}."
            raise TypeError(msg)

        style = self.style
        if style is not None:
            if not isinstance(style, str):
                msg = f"style must be a string or None, got {type(style).__name__}."
                raise TypeError(msg)
            if style not in _STYLE_PRESETS:
                msg = f"Invalid style: {style!r}. Must be one of {list(_STYLE_PRESETS)} or None."
                raise ValueError(msg)

        lang = self.lang
        if not isinstance(lang, str):
            msg = f"lang must be a string, got {type(lang).__name__}."
            raise TypeError(msg)
        if lang not in _VALID_LANGS:
            msg = f"Invalid lang: {lang!r}. Must be one of {sorted(_VALID_LANGS)}."
            raise ValueError(msg)

        emoji_mode = self.emoji_mode
        if not isinstance(emoji_mode, str):
            msg = f"emoji_mode must be a string, got {type(emoji_mode).__name__}."
            raise TypeError(msg)
        if emoji_mode not in _VALID_EMOJI_MODES:
            msg = (
                f"Invalid emoji_mode: {emoji_mode!r}. Must be one of {sorted(_VALID_EMOJI_MODES)}."
            )
            raise ValueError(msg)

        object.__setattr__(self, "stopwords", _coerce_stopwords(self.stopwords))
        object.__setattr__(self, "replacements", _coerce_replacements(self.replacements))

    @classmethod
    def from_kwargs(cls, **kwargs: Any) -> SlugConfig:
        """Build a validated SlugConfig from keyword arguments.

        Validates all fields and merges style presets with explicit
        overrides (explicit kwargs take precedence). Passing ``None`` for
        any field means "not provided": the style preset's value is used
        when a style is active, otherwise the field default.

        Args:
            **kwargs: Configuration fields as keyword arguments.

        Returns:
            A frozen SlugConfig instance.

        Raises:
            ValueError: If an invalid style, lang, emoji_mode, empty
                separator, separator containing alphanumeric or whitespace
                characters, negative ``max_length``, or empty replacement
                key is provided.
            TypeError: If a field receives a value of the wrong type
                (e.g. non-bool flag, non-int ``max_length``, non-string
                ``fallback``, malformed ``replacements`` or ``stopwords``
                entries).
        """
        style = kwargs.get("style")
        if style is not None:
            if not isinstance(style, str):
                msg = f"style must be a string or None, got {type(style).__name__}."
                raise TypeError(msg)
            if style not in _STYLE_PRESETS:
                msg = f"Invalid style: {style!r}. Must be one of {list(_STYLE_PRESETS)} or None."
                raise ValueError(msg)

        separator = kwargs.get("separator")
        if separator is not None:
            if not isinstance(separator, str):
                msg = f"separator must be a string, got {type(separator).__name__}."
                raise TypeError(msg)
            if not separator:
                msg = "separator must be a non-empty string."
                raise ValueError(msg)

        for key in _NONE_MEANS_DEFAULT:
            if kwargs.get(key) is None:
                kwargs.pop(key, None)

        if style is not None:
            preset = _STYLE_PRESETS[style]
            merged: dict[str, Any] = dict(preset)
            for key, value in kwargs.items():
                if key in ("separator", "lowercase"):
                    if value is not None:
                        merged[key] = value
                elif value != _CONFIG_DEFAULTS.get(key):
                    merged[key] = value
            kwargs = merged

        if kwargs.get("separator") is None:
            kwargs["separator"] = "-"
        if kwargs.get("lowercase") is None:
            kwargs["lowercase"] = True

        return cls(**kwargs)


_CONFIG_DEFAULTS: dict[str, object] = {
    f.name: f.default
    for f in dataclasses.fields(SlugConfig)
    if f.default is not dataclasses.MISSING
}
