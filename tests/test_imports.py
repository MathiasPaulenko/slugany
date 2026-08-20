from __future__ import annotations

import slugany


class TestImports:
    def test_import_slugify(self) -> None:
        from slugany import slugify

        assert callable(slugify)

    def test_import_slugify_batch(self) -> None:
        from slugany import slugify_batch

        assert callable(slugify_batch)

    def test_import_is_slug(self) -> None:
        from slugany import is_slug

        assert callable(is_slug)

    def test_import_slugconfig(self) -> None:
        from slugany import SlugConfig

        assert SlugConfig is not None

    def test_version(self) -> None:
        assert slugany.__version__ == "1.0.0"

    def test_all(self) -> None:
        assert "slugify" in slugany.__all__
        assert "slugify_batch" in slugany.__all__
        assert "is_slug" in slugany.__all__
        assert "SlugConfig" in slugany.__all__
        assert "__version__" in slugany.__all__

    def test_slug_in_all_when_pydantic_available(self) -> None:
        try:
            import pydantic  # noqa: F401

            assert "Slug" in slugany.__all__
        except ImportError:
            assert "Slug" not in slugany.__all__

    def test_init_import_error_fallback(self) -> None:
        import builtins
        import importlib
        from unittest.mock import patch

        original_import = builtins.__import__

        def mock_import(name: str, *args: object, **kwargs: object) -> object:
            if name == "slugany._pydantic":
                raise ImportError("mocked")
            return original_import(name, *args, **kwargs)  # type: ignore[call-arg]

        with patch("builtins.__import__", side_effect=mock_import):
            importlib.reload(slugany)
            assert "Slug" not in slugany.__all__

        importlib.reload(slugany)
