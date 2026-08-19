from __future__ import annotations

from typing import Annotated, Any

try:
    from pydantic import BeforeValidator

    from slugany import slugify

    Slug: Any = Annotated[str, BeforeValidator(lambda v: slugify(v) if isinstance(v, str) else v)]
except ImportError:
    Slug = str
