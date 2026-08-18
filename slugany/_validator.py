from __future__ import annotations

import re


def is_slug(s: str, separator: str = "-", *, allow_unicode: bool = False) -> bool:
    """Check whether a string is a valid slug.

    A valid slug contains only alphanumeric characters (ASCII or Unicode
    when ``allow_unicode`` is ``True``) separated by the given separator,
    with no leading or trailing separators.

    Args:
        s: The string to validate.
        separator: The separator used in the slug. Defaults to ``"-"``.
        allow_unicode: If ``True``, allow Unicode word characters (``\\w``)
            in addition to ASCII alphanumeric characters.

    Returns:
        ``True`` if the string is a valid slug, ``False`` otherwise.
    """
    if not s:
        return False
    sep = re.escape(separator)
    char_class = r"\w" if allow_unicode else r"a-zA-Z0-9"
    return bool(re.match(f"^[{char_class}]+({sep}[{char_class}]+)*$", s))
