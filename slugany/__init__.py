from slugany._config import SlugConfig
from slugany._slugify import slugify, slugify_batch
from slugany._validator import is_slug

__version__ = "0.2.0"

__all__ = ["slugify", "slugify_batch", "is_slug", "SlugConfig", "__version__"]

try:
    import pydantic  # noqa: F401

    from slugany._pydantic import Slug  # noqa: F401

    __all__.append("Slug")
except ImportError:
    pass
