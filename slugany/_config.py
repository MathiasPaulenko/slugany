from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class SlugConfig:
    separator: str = "-"
    lowercase: bool = True
    max_length: int = 0
    word_boundary: bool = False
    stopwords: frozenset[str] = field(default_factory=frozenset)
    allow_unicode: bool = False
    replacements: frozenset[tuple[str, str]] = field(default_factory=frozenset)
    style: str | None = None
    lang: str = "auto"
    fallback: str = ""
    emoji_mode: str = "strip"
    css_safe: bool = False
    html_entities: bool = True
    smart_punctuation: bool = True

    @classmethod
    def from_kwargs(cls, **kwargs: object) -> SlugConfig:
        style = kwargs.get("style")
        if style is not None and style not in _STYLE_PRESETS:
            msg = f"Invalid style: {style!r}. Must be one of {list(_STYLE_PRESETS)} or None."
            raise ValueError(msg)

        lang = kwargs.get("lang", "auto")
        if lang not in ("auto", "es", "pt", "de", "fr", "it"):
            msg = f"Invalid lang: {lang!r}. Must be one of auto/es/pt/de/fr/it."
            raise ValueError(msg)

        emoji_mode = kwargs.get("emoji_mode", "strip")
        if emoji_mode not in ("strip", "text", "keep"):
            msg = f"Invalid emoji_mode: {emoji_mode!r}. Must be strip/text/keep."
            raise ValueError(msg)

        separator = kwargs.get("separator", "-")
        if not isinstance(separator, str) or not separator:
            msg = "separator must be a non-empty string."
            raise ValueError(msg)

        replacements = kwargs.get("replacements")
        if replacements is not None:
            if isinstance(replacements, dict):
                replacements = frozenset(replacements.items())
            else:
                replacements = frozenset(replacements)  # type: ignore[call-overload]
            kwargs["replacements"] = replacements

        stopwords = kwargs.get("stopwords")
        if stopwords is not None:
            kwargs["stopwords"] = frozenset(stopwords)  # type: ignore[call-overload]

        if style is not None:
            preset = _STYLE_PRESETS[style]
            merged: dict[str, object] = dict(preset)
            merged.update(kwargs)
            kwargs = merged

        return cls(**kwargs)  # type: ignore[arg-type]


_STYLE_PRESETS: dict[str, dict[str, object]] = {
    "url": {"separator": "-", "lowercase": True},
    "filename": {"separator": "-", "lowercase": False},
    "kebab": {"separator": "-", "lowercase": True},
    "snake": {"separator": "_", "lowercase": True},
    "camel": {"separator": "-", "lowercase": True, "style": "camel"},
    "pascal": {"separator": "-", "lowercase": False, "style": "pascal"},
    "dot": {"separator": ".", "lowercase": True},
    "train": {"separator": "-", "lowercase": False, "style": "train"},
}
