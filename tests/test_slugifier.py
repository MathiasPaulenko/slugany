from __future__ import annotations

import dataclasses

import pytest

from slugany import SlugConfig, Slugifier, slugify


class TestSlugifier:
    def test_basic(self) -> None:
        s = Slugifier.style("camel")
        assert s("hello world") == "helloWorld"

    def test_reuse(self) -> None:
        s = Slugifier.style("kebab")
        assert s("hello world") == "hello-world"
        assert s("foo bar baz") == "foo-bar-baz"

    def test_style_factory(self) -> None:
        s = Slugifier.style("snake", max_length=5, word_boundary=True)
        assert s("hello world foo") == "hello"

    def test_config_property(self) -> None:
        s = Slugifier.style("camel")
        assert isinstance(s.config, SlugConfig)
        assert s.config.style == "camel"

    def test_config_immutable(self) -> None:
        s = Slugifier.style("camel")
        with pytest.raises(dataclasses.FrozenInstanceError):
            s.config.separator = "_"  # type: ignore[misc]

    def test_slots_raises_attribute_error(self) -> None:
        s = Slugifier.style("camel")
        with pytest.raises(AttributeError):
            s.foo = 1  # type: ignore[attr-defined]

    def test_same_as_slugify(self) -> None:
        s = Slugifier.style("camel")
        assert s("Café résumé") == slugify("Café résumé", style="camel")

    def test_call_non_string_raises(self) -> None:
        s = Slugifier()
        with pytest.raises(TypeError, match="text must be a string"):
            s(123)  # type: ignore[arg-type]

    def test_repr(self) -> None:
        s = Slugifier.style("camel")
        assert "Slugifier" in repr(s)
        assert "camel" in repr(s)

    def test_shares_lru_cache(self) -> None:
        """Slugifier calls use the same lru_cache as slugify()."""
        slugify.cache_clear()
        s = Slugifier.style("kebab")
        s("Hello World")
        s("Hello World")
        info = slugify.cache_info()
        assert info.hits == 1
        # identical slugify() call with the same config hits the same cache entry
        slugify("Hello World", style="kebab")
        assert slugify.cache_info().hits == 2
        slugify.cache_clear()
