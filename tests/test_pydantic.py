from __future__ import annotations

import importlib
from unittest.mock import patch

import pytest

try:
    import pydantic  # noqa: F401

    _PYDANTIC_AVAILABLE = True
except ImportError:
    _PYDANTIC_AVAILABLE = False


@pytest.mark.skipif(not _PYDANTIC_AVAILABLE, reason="pydantic not installed")
class TestPydanticSlug:
    def test_pydantic_slug_type(self) -> None:
        from pydantic import BaseModel

        from slugany import Slug

        class Article(BaseModel):
            title: Slug

        article = Article(title="Hello World!")
        assert article.title == "hello-world"

    def test_pydantic_slug_already_slug(self) -> None:
        from pydantic import BaseModel

        from slugany import Slug

        class Article(BaseModel):
            title: Slug

        article = Article(title="already-a-slug")
        assert article.title == "already-a-slug"


class TestSlugWithoutPydantic:
    def test_slug_is_str_without_pydantic(self) -> None:
        with patch.dict("sys.modules", {"pydantic": None}):
            import slugany._pydantic as mod

            importlib.reload(mod)
            assert mod.Slug is str

        import slugany._pydantic as mod

        importlib.reload(mod)
