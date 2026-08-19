from __future__ import annotations

import pytest

from slugany import slugify_batch


class TestSlugifyBatch:
    def test_basic(self) -> None:
        assert slugify_batch(["Hello World", "Caf\u00e9"]) == ["hello-world", "cafe"]

    def test_empty(self) -> None:
        assert slugify_batch([]) == []

    def test_single(self) -> None:
        assert slugify_batch(["Hello World"]) == ["hello-world"]

    def test_custom_kwargs(self) -> None:
        assert slugify_batch(["Hello World", "Foo Bar"], separator="_") == [
            "hello_world",
            "foo_bar",
        ]

    def test_mixed(self) -> None:
        assert slugify_batch(["Hello World", "", "!!!"]) == ["hello-world", "", ""]

    def test_tuple(self) -> None:
        assert slugify_batch(("Hello World", "Caf\u00e9")) == ["hello-world", "cafe"]

    def test_generator(self) -> None:
        assert slugify_batch(x for x in ["Hello World", "Caf\u00e9"]) == [
            "hello-world",
            "cafe",
        ]

    def test_type_error_on_non_string(self) -> None:
        with pytest.raises(TypeError):
            slugify_batch([123])  # type: ignore[list-item]

    def test_explicit_kwargs(self) -> None:
        assert slugify_batch(
            ["Hello World", "Foo Bar"],
            separator="_",
            lowercase=False,
            style="pascal",
        ) == ["HelloWorld", "FooBar"]

    def test_batch_generator(self) -> None:
        from collections.abc import Iterator

        def gen() -> Iterator[str]:
            yield "Hello World"
            yield "Foo Bar"

        assert slugify_batch(gen()) == ["hello-world", "foo-bar"]

    def test_batch_large(self) -> None:
        items = [f"Item {i} Test" for i in range(100)]
        expected = [f"item-{i}-test" for i in range(100)]
        assert slugify_batch(items) == expected

    def test_batch_iterator(self) -> None:
        assert slugify_batch(iter(["Hello", "World"])) == ["hello", "world"]
