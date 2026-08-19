from __future__ import annotations

from slugany import slugify


class TestStopwords:
    def test_basic(self) -> None:
        assert slugify("the quick fox", stopwords=["the"]) == "quick-fox"

    def test_case_insensitive(self) -> None:
        assert slugify("THE Quick Fox", stopwords=["the"]) == "quick-fox"

    def test_multiple(self) -> None:
        assert slugify("the quick brown fox", stopwords=["the", "fox"]) == "quick-brown"

    def test_no_stopwords(self) -> None:
        assert slugify("the quick fox", stopwords=[]) == "the-quick-fox"

    def test_stopword_at_end(self) -> None:
        assert slugify("quick fox the", stopwords=["the"]) == "quick-fox"

    def test_all_stopwords(self) -> None:
        assert slugify("the the the", stopwords=["the"]) == ""

    def test_with_lowercase_false(self) -> None:
        assert slugify("The Quick Fox", stopwords=["the"], lowercase=False) == "Quick-Fox"

    def test_stopword_in_middle(self) -> None:
        assert slugify("quick the fox", stopwords=["the"]) == "quick-fox"
