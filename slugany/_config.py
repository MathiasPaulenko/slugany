from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Any

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


@dataclass(frozen=True, slots=True)
class SlugConfig:
    """Immutable configuration for the slugify pipeline.

    All fields have sensible defaults. Use :meth:`from_kwargs` to create
    a config from keyword arguments with validation and style preset merging.
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

    @classmethod
    def from_kwargs(cls, **kwargs: Any) -> SlugConfig:
        """Build a validated SlugConfig from keyword arguments.

        Validates style, lang, emoji_mode, and separator. Merges style
        presets with explicit overrides (explicit kwargs take precedence).

        Args:
            **kwargs: Configuration fields as keyword arguments.

        Returns:
            A frozen SlugConfig instance.

        Raises:
            ValueError: If an invalid style, lang, emoji_mode, empty
                separator, or empty replacement key is provided.
        """
        style = kwargs.get("style")
        if style is not None and style not in _STYLE_PRESETS:
            msg = f"Invalid style: {style!r}. Must be one of {list(_STYLE_PRESETS)} or None."
            raise ValueError(msg)

        lang = kwargs.get("lang", "auto")
        if lang not in _VALID_LANGS:
            msg = f"Invalid lang: {lang!r}. Must be one of {sorted(_VALID_LANGS)}."
            raise ValueError(msg)

        emoji_mode = kwargs.get("emoji_mode", "strip")
        if emoji_mode not in _VALID_EMOJI_MODES:
            msg = (
                f"Invalid emoji_mode: {emoji_mode!r}. Must be one of {sorted(_VALID_EMOJI_MODES)}."
            )
            raise ValueError(msg)

        separator = kwargs.get("separator")
        if separator is not None and (not isinstance(separator, str) or not separator):
            msg = "separator must be a non-empty string."
            raise ValueError(msg)
        if separator is not None and any(c.isalnum() for c in separator):
            msg = f"separator must not contain alphanumeric characters, got {separator!r}."
            raise ValueError(msg)

        fallback = kwargs.get("fallback")
        if fallback is not None and not isinstance(fallback, str):
            msg = f"fallback must be a string, got {type(fallback).__name__}."
            raise TypeError(msg)

        max_length = kwargs.get("max_length")
        if max_length is not None and (
            not isinstance(max_length, int) or isinstance(max_length, bool)
        ):
            msg = f"max_length must be an integer, got {type(max_length).__name__}."
            raise TypeError(msg)

        for bool_field in (
            "lowercase",
            "word_boundary",
            "allow_unicode",
            "css_safe",
            "html_entities",
            "smart_punctuation",
        ):
            val = kwargs.get(bool_field)
            if val is not None and not isinstance(val, bool):
                msg = f"{bool_field} must be a boolean, got {type(val).__name__}."
                raise TypeError(msg)

        replacements = kwargs.get("replacements")
        if replacements is not None:
            if isinstance(replacements, dict):
                replacements = tuple(replacements.items())
            else:
                replacements = tuple(replacements)
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
            kwargs["replacements"] = replacements
        else:
            kwargs.pop("replacements", None)

        stopwords = kwargs.get("stopwords")
        if stopwords is not None:
            kwargs["stopwords"] = frozenset(stopwords)
        else:
            kwargs.pop("stopwords", None)

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
