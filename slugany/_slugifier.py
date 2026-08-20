from __future__ import annotations

from typing import Any

from slugany._config import SlugConfig
from slugany._pipeline import _run_pipeline


class Slugifier:
    """Stateless slugifier bound to a fixed configuration.

    Created via :meth:`Slugifier.style` or the constructor with a
    :class:`SlugConfig`. The instance is callable — calling it with
    a string runs the slugify pipeline using the stored config.

    The ``config`` attribute is read-only; the underlying
    :class:`SlugConfig` is frozen and cannot be mutated.

    Examples:
        >>> s = Slugifier.style("camel")
        >>> s("hello world")
        'helloWorld'
    """

    __slots__ = ("_config",)

    def __init__(self, config: SlugConfig | None = None) -> None:
        """Initialize the Slugifier with an optional configuration.

        Args:
            config: A :class:`SlugConfig` instance. If ``None``, defaults
                to ``SlugConfig()``.
        """
        self._config = config or SlugConfig()

    @property
    def config(self) -> SlugConfig:
        """The frozen, read-only configuration for this slugifier."""
        return self._config

    @classmethod
    def style(cls, style: str, **overrides: Any) -> Slugifier:
        """Create a Slugifier from a named style preset.

        Args:
            style: One of ``kebab``, ``snake``, ``camel``, ``pascal``,
                ``dot``, ``train``, ``filename``, ``url``.
            **overrides: Additional keyword arguments forwarded to
                :meth:`SlugConfig.from_kwargs`.

        Returns:
            A Slugifier bound to the resolved configuration.
        """
        return cls(SlugConfig.from_kwargs(style=style, **overrides))

    def __call__(self, text: str) -> str:
        """Slugify *text* using this slugifier's configuration.

        Args:
            text: The text to slugify. Must be a string.

        Returns:
            The slugified string.

        Raises:
            TypeError: If ``text`` is not a string.
        """
        if not isinstance(text, str):
            msg = f"text must be a string, got {type(text).__name__}"
            raise TypeError(msg)
        return _run_pipeline(text, self._config)

    def __repr__(self) -> str:
        return f"Slugifier(config={self._config!r})"
