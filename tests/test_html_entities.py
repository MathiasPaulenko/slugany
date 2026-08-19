from __future__ import annotations

from slugany import slugify


class TestHtmlEntities:
    def test_amp(self) -> None:
        assert slugify("Tom &amp; Jerry") == "tom-jerry"

    def test_numeric_decimal(self) -> None:
        assert slugify("caf&#233;") == "cafe"

    def test_numeric_hex(self) -> None:
        assert slugify("caf&#xE9;") == "cafe"

    def test_nbsp(self) -> None:
        assert slugify("hello&nbsp;world") == "hello-world"

    def test_lt_gt(self) -> None:
        assert slugify("a &lt; b &gt; c") == "a-b-c"

    def test_disabled(self) -> None:
        assert slugify("Tom &amp; Jerry", html_entities=False) == "tom-amp-jerry"

    def test_multiple_entities(self) -> None:
        assert slugify("&lt;div&gt;Hello&amp;World&lt;/div&gt;") == "div-hello-world-div"
