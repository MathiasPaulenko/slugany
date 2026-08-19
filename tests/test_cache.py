from __future__ import annotations

from slugany import slugify


class TestCache:
    def setup_method(self) -> None:
        slugify.cache_clear()

    def test_cache_hit(self) -> None:
        slugify("Hello World")
        info_after_first = slugify.cache_info()
        slugify("Hello World")
        info_after_second = slugify.cache_info()
        assert info_after_second.hits == info_after_first.hits + 1

    def test_cache_miss(self) -> None:
        slugify("Hello World")
        info = slugify.cache_info()
        assert info.misses >= 1

    def test_cache_clear(self) -> None:
        slugify("Hello World")
        slugify.cache_clear()
        info = slugify.cache_info()
        assert info.currsize == 0

    def test_different_args(self) -> None:
        slugify("Hello World")
        slugify("Hello World", separator="_")
        info = slugify.cache_info()
        assert info.currsize >= 2

    def test_same_args(self) -> None:
        slugify("Hello World")
        slugify("Hello World")
        info = slugify.cache_info()
        assert info.currsize == 1

    def test_different_separator(self) -> None:
        slugify("Hello World")
        slugify("Hello World", separator="_")
        info = slugify.cache_info()
        assert info.misses == 2

    def test_different_lang(self) -> None:
        slugify("España")
        slugify("España", lang="es")
        info = slugify.cache_info()
        assert info.misses == 2

    def test_same_args_hit(self) -> None:
        slugify("Hello World", separator="_", lowercase=False)
        slugify("Hello World", separator="_", lowercase=False)
        info = slugify.cache_info()
        assert info.hits == 1

    def test_cache_clear_resets(self) -> None:
        slugify("Hello World")
        slugify("Hello World")
        slugify.cache_clear()
        info = slugify.cache_info()
        assert info.hits == 0
        assert info.currsize == 0
