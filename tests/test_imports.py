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
        assert slugany.__version__ == "0.1.0"

    def test_all(self) -> None:
        assert "slugify" in slugany.__all__
        assert "slugify_batch" in slugany.__all__
        assert "is_slug" in slugany.__all__
        assert "SlugConfig" in slugany.__all__
        assert "__version__" in slugany.__all__
