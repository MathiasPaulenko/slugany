from slugany._config import SlugConfig
from slugany._slugify import slugify, slugify_batch
from slugany._validator import is_slug

__version__ = "0.1.0"

__all__ = ["slugify", "slugify_batch", "is_slug", "SlugConfig", "__version__"]

try:
    from slugany._pydantic import Slug  # noqa: F401

    __all__.append("Slug")
except ImportError:
    pass
