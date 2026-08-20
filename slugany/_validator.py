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
            and emoji characters in addition to ASCII alphanumeric characters.

    Returns:
        ``True`` if the string is a valid slug, ``False`` otherwise.

    Raises:
        TypeError: If ``s`` or ``separator`` is not a string.

    Examples:
        >>> is_slug("hello-world")
        True
        >>> is_slug("hello world")
        False
        >>> is_slug("hello_world", separator="_")
        True
    """
    if not isinstance(s, str):
        msg = f"s must be a string, got {type(s).__name__}"
        raise TypeError(msg)
    if not isinstance(separator, str):
        msg = f"separator must be a string, got {type(separator).__name__}"
        raise TypeError(msg)
    if not s:
        return False
    if allow_unicode:
        char_class = r"\w"
        extra = (
            r"\U0001f000-\U0001faff"
            r"\u2600-\u27bf"
            r"\u00a9\u00ae\u203c\u2049\u2122\u2139"
            r"\u2194-\u2199\u21a9\u21aa\u24c2"
            r"\u25aa\u25ab\u25b6\u25c0\u25fb-\u25fe"
            r"\u0300-\u036f"
            r"\u0483-\u0489"
            r"\u0591-\u05bd\u05bf\u05c1-\u05c2\u05c4-\u05c5\u05c7"
            r"\u0610-\u061a\u064b-\u065f\u0670\u06d6-\u06dc\u06df-\u06e4"
            r"\u06e7-\u06e8\u06ea-\u06ed\u0711\u0730-\u074a\u07a6-\u07b0"
            r"\u07eb-\u07f3\u07fd\u0816-\u0819\u081b-\u0823\u0825-\u0827"
            r"\u0829-\u082d\u0859-\u085b\u0897-\u089f\u08ca-\u08e1\u08e3-\u0903"
            r"\u093a-\u093c\u093e-\u094f\u0951-\u0957\u0962-\u0963"
            r"\u0981-\u0983\u09bc\u09be-\u09c4\u09c7-\u09c8\u09cb-\u09cd"
            r"\u09d7\u09e2-\u09e3\u09fe\u0a01-\u0a03\u0a3c\u0a3e-\u0a42"
            r"\u0a47-\u0a48\u0a4b-\u0a4d\u0a51\u0a70-\u0a71\u0a75"
            r"\u0a81-\u0a83\u0abc\u0abe-\u0ac5\u0ac7-\u0ac9\u0acb-\u0acd"
            r"\u0ae2-\u0ae3\u0afa-\u0aff\u0b01-\u0b03\u0b3c\u0b3e-\u0b44"
            r"\u0b47-\u0b48\u0b4b-\u0b4d\u0b55-\u0b57\u0b62-\u0b63"
            r"\u0b82\u0bbe-\u0bc2\u0bc6-\u0bc8\u0bca-\u0bcd\u0bd7"
            r"\u0c00-\u0c04\u0c3c\u0c3e-\u0c44\u0c46-\u0c48\u0c4a-\u0c4d"
            r"\u0c55-\u0c56\u0c62-\u0c63\u0c81-\u0c83\u0cbc\u0cbe-\u0cc4"
            r"\u0cc6-\u0cc8\u0cca-\u0ccd\u0cd5-\u0cd6\u0ce2-\u0ce3\u0cf3"
            r"\u0d00-\u0d03\u0d3b-\u0d3c\u0d3e-\u0d44\u0d46-\u0d48"
            r"\u0d4a-\u0d4d\u0d57\u0d62-\u0d63\u0d81-\u0d83\u0dca"
            r"\u0dcf-\u0dd4\u0dd6\u0dd8-\u0ddf\u0df2-\u0df3"
            r"\u0e31\u0e34-\u0e3a\u0e47-\u0e4e\u0eb1\u0eb4-\u0ebc\u0ec8-\u0ece"
            r"\u0f18-\u0f19\u0f35\u0f37\u0f39\u0f3e-\u0f3f\u0f71-\u0f84"
            r"\u0f86-\u0f87\u0f8d-\u0f97\u0f99-\u0fbc\u0fc6"
            r"\u102b-\u103e\u1056-\u1059\u105e-\u1060\u1062-\u1064"
            r"\u1067-\u106d\u1071-\u1074\u1082-\u108d\u108f\u109a-\u109d"
            r"\u135d-\u135f\u1712-\u1715\u1732-\u1734\u1752-\u1753\u1772-\u1773"
            r"\u17b4-\u17d3\u17dd\u180b-\u180d\u180f\u1885-\u1886\u18a9"
            r"\u1920-\u192b\u1930-\u193b\u1a17-\u1a1b\u1a55-\u1a5e"
            r"\u1a60-\u1a7c\u1a7f\u1ab0-\u1ace\u1b00-\u1b04\u1b34-\u1b44"
            r"\u1b6b-\u1b73\u1b80-\u1b82\u1ba1-\u1bad\u1be6-\u1bf3"
            r"\u1c24-\u1c37\u1cd0-\u1cd2\u1cd4-\u1ce8\u1ced\u1cf4\u1cf7-\u1cf9"
            r"\u1dc0-\u1dff\u20d0-\u20f0\u2cef-\u2cf1\u2d7f\u2de0-\u2dff"
            r"\u302a-\u302f\u3099-\u309a"
        )
        if not separator:
            return bool(re.match(f"^[{char_class}{extra}]+$", s))
        sep = re.escape(separator)
        return bool(re.match(f"^[{char_class}{extra}]+({sep}[{char_class}{extra}]+)*$", s))
    char_class = r"a-zA-Z0-9"
    if not separator:
        return bool(re.match(f"^[{char_class}]+$", s))
    sep = re.escape(separator)
    return bool(re.match(f"^[{char_class}]+({sep}[{char_class}]+)*$", s))
