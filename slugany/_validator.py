from __future__ import annotations

import re


def is_slug(s: str, separator: str = "-") -> bool:
    if not s:
        return False
    sep = re.escape(separator)
    return bool(re.match(f"^[a-zA-Z0-9]+({sep}[a-zA-Z0-9]+)*$", s))
