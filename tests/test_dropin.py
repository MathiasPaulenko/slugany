from __future__ import annotations

import pytest

from slugany import slugify


class TestDropInCompat:
    def test_basic(self) -> None:
        assert slugify("Hello World") == "hello-world"

    def test_numbers(self) -> None:
        assert slugify("Hello 123 World") == "hello-123-world"

    def test_special_chars(self) -> None:
        assert slugify("Hello @ World #!") == "hello-world"

    def test_multiple_spaces(self) -> None:
        assert slugify("Hello    World") == "hello-world"

    def test_leading_trailing(self) -> None:
        assert slugify("   Hello World   ") == "hello-world"

    def test_custom_separator(self) -> None:
        assert slugify("Hello World", separator="_") == "hello_world"

    def test_max_length(self) -> None:
        assert slugify("hello-world-foo", max_length=10) == "hello-worl"

    def test_no_lowercase(self) -> None:
        assert slugify("Hello World", lowercase=False) == "Hello-World"

    def test_empty(self) -> None:
        assert slugify("") == ""

    def test_unicode(self) -> None:
        assert slugify("Caf\u00e9 r\u00e9sum\u00e9") == "cafe-resume"

    def test_idempotent(self) -> None:
        result = slugify("Hello World!!!")
        assert slugify(result) == result

    def test_keyword_only(self) -> None:
        with pytest.raises(TypeError):
            slugify("Hello World", "_")  # type: ignore[misc]
