from importlib.metadata import PackageNotFoundError, version

from slugany._config import SlugConfig
from slugany._slugifier import Slugifier
from slugany._slugify import deconfuse, slugify, slugify_batch
from slugany._validator import is_slug

try:
    __version__ = version("slugany")
except PackageNotFoundError:
    __version__ = "0.0.0+local"

__all__ = [
    "slugify",
    "slugify_batch",
    "is_slug",
    "SlugConfig",
    "Slugifier",
    "deconfuse",
    "__version__",
]

try:
    import pydantic  # noqa: F401

    from slugany._pydantic import Slug  # noqa: F401

    __all__.append("Slug")
except ImportError:
    pass
